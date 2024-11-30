import json
import os
from typing import List, Optional, Any, Dict

import psycopg2
from uuid_extensions import uuid7str
from datetime import datetime
from job.job import Job, JobType, JobStatus
from config import DB_CONFIG


class DatabaseManager:
    def __init__(self):
        """
        Initialize a DatabaseManager instance.

        The DatabaseManager instance is initialized with no existing connection to
        the PostgreSQL database. The connection is established on demand by calling
        the get_connector() method.

        Attributes:
            conn: A psycopg2 connection object, or None if no connection has been
                established yet.
        """
        self.conn = None

    def get_connector(self):
        """
        Get a connection to the PostgreSQL database. If no connection exists yet,
        try to create a new one with the DB_CONFIG from config.py file. If the
        connection is closed for any reason, try to reopen it.

        Returns:
            connection: A psycopg2 connection object.

        Raises:
            psycopg2.Error: If the database connection fails.
        """
        if self.conn is None or self.conn.closed:
            try:
                self.conn = psycopg2.connect(**DB_CONFIG)
            except psycopg2.Error as e:
                print(f"Error connecting to database: {e}")
                raise Exception(f"Error in get_connector(): {e}")
        return self.conn

    def close_connection(self):
        """
        Close the current connection to the PostgreSQL database, if one exists.

        If a connection has been established, this method will close it. If no
        connection has been established, this method does nothing.

        Returns:
            None
        """
        if self.conn:
            self.conn.close()
            self.conn = None

    def get_jobs(
        self,
        job_type: JobType,
        statuses: List[JobStatus] = [JobStatus.NEW, JobStatus.DONE],
    ) -> Optional[List[Job]]:
        """
        Get a list of jobs of the given type from the database.
        Loaded jobs statuses will be updated to 'processing' after load.

        The list will be ordered by the job creation time in ascending order.

        Args:
            job_type: The type of jobs to retrieve.
            statuses: The statuses of the jobs to retrieve. Defaults to [JobStatus.NEW, JobStatus.PROCESSING].

        Returns:
            A list of Job objects, or None if no jobs are found.
        Raises:
            psycopg2.Error: If the database connection fails.
        """
        conn = self.get_connector()
        try:
            with conn.cursor() as cursor:
                statuses_str = ", ".join(f"'{status.name}'" for status in statuses)
                cursor.execute(
                    f"""
                    SELECT id, job_type, job_status, args
                    FROM job
                    WHERE job_type = '{job_type.name}' AND job_status IN ({statuses_str})
                    ORDER BY id ASC;
                    """
                )
                raw_jobs: list[tuple[Any, ...]] = cursor.fetchall()
                if raw_jobs:
                    jobs: List[Job] = []
                    for raw_job in raw_jobs:
                        (
                            job_id,
                            job_type,
                            job_status,
                            args
                        ) = raw_job
                        jobs.append(
                            Job(
                                id=job_id,
                                type=JobType[job_type.upper()],
                                status=JobStatus[job_status.upper()],
                                args=args
                            )
                        )
                    return jobs
        except psycopg2.Error as e:
            print(f"Error getting jobs of type '{job_type}': {e}")
            raise Exception(f"Error in get_jobs(): {e}")

    def update_job_status(self, job_id: str, new_status: JobStatus) -> None:
        """
        Updates the status of a job with the given job_id to the given new_status.

        Args:
            job_id (str): The ID of the job to be updated.
            new_status (Jobstatus): The new status of the job.

        Raises:
            psycopg2.Error: If the database connection fails.
        """
        conn = self.get_connector()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE job
                    SET status = '{new_status.value}'
                    WHERE id = '{job_id}'
                    """
                )
                conn.commit()
        except psycopg2.Error as e:
            print(f"Error updating status of job '{job_id}': {e}")
            conn.rollback()

    def update_job_check_time(self, job_id: str) -> None:
        """
        Updates the check_time of a job with the given job_id to the current time.

        Args:
            job_id (str): The ID of the job to be updated.

        Raises:
            psycopg2.Error: If the database connection fails.
        """
        conn = self.get_connector()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE job
                    SET check_time = NOW()
                    WHERE id = '{job_id}'
                    """
                )
                conn.commit()
        except psycopg2.Error as e:
            print(f"Error updating check time of job '{job_id}': {e}")
            conn.rollback()

    # TODO: Add Stake class.
    def save_stakes(self, job_id: str, stakes: List[Dict[str, Any]]) -> None:
        """
        Saves a list of stake stakes to the stake table.

        Args:
            stakes (List[Dict[str, Any]]): A list of dictionaries, where each dictionary
                contains the following keys:
                    - job_id (str): The ID of the job that requested the validation.
                    - timestamp (datetime): The timestamp of the stake.
                    - crypto_price (float): The price of the cryptocurrency at the time of
                        the stake.
                    - usdt_diff (float): The difference in USDT balance after stake.
                    - crypto_diff (float): The difference in cryptocurrency balance after stake.

        Raises:
            psycopg2.Error: If the database connection fails.
        """
        conn = self.get_connector()
        try:
            with conn.cursor() as cursor:
                insert_query = """
                    INSERT INTO stake (id, job_id, time, crypto_price, usdt_diff, crypto_diff)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                data_to_insert = [
                    (
                        uuid7str(),
                        job_id,
                        stake["timestamp"],  # in db it's called time.
                        stake[
                            "current_crypto_price"
                        ],  # in db it's called crypto_price.
                        stake["usdt_diff"],
                        stake["crypto_diff"],
                    )
                    for stake in stakes
                ]
                cursor.executemany(insert_query, data_to_insert)
                conn.commit()
        except psycopg2.Error as e:
            print(f"Error inserting into stake: {e}")
            conn.rollback()

    def update_job_params(self, job_id: str, params: Dict[str, Any]) -> None:
        """
        Updates the params of a job with the given job_id to the given params.

        Args:
            job_id (str): The ID of the job to be updated.
            params (Dict[str, Any]): The new params of the job.

        Raises:
            psycopg2.Error: If the database connection fails.
        """
        conn = self.get_connector()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE job
                    SET params = '{json.dumps(params)}'
                    WHERE id = '{job_id}'
                    """
                )
                conn.commit()
        except psycopg2.Error as e:
            print(f"Error updating params of job '{job_id}': {e}")
            conn.rollback()

    def save_pnl(self, job_id: str, trading_results: Dict[str, Any]) -> None:
        """
        Saves a record of profit and loss to the pnl table.

        Args:
            job_id (str): The ID of the job that requested the validation.
            trading_results (Dict[str, Any]): A dictionary containing the following keys:
                - start_date (datetime): The timestamp of the start of validation on data.
                - end_date (datetime): The timestamp of the end of validation on data.
                - start_balance (float): The starting balance of the validation.
                - end_balance (float): The ending balance of the validation.

        Raises:
            psycopg2.Error: If the database connection fails.
        """
        conn = self.get_connector()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO pnl (id, job_id, start_date, end_date, start_balance, end_balance)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        uuid7str(),
                        job_id,
                        trading_results["start_date"],
                        trading_results["end_date"],
                        trading_results["start_balance"],
                        trading_results["end_balance"],
                    ),
                )
                conn.commit()
        except psycopg2.Error as e:
            print(f"Error inserting into pnl: {e}")
            conn.rollback()

    def get_job_last_stake_time(self, job_id: str) -> Optional[datetime]:
        """
        Fetch the last stake time from the database.

        Args:
            job_id: The ID of the job.

        Returns:
            The last stake time as a datetime object, or None if no stakes exist.
        """
        conn = self.get_connector()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT stake.time
                    FROM stake
                    INNER JOIN job ON job.id = stake.job_id
                    WHERE job_id = '{job_id}'
                    ORDER BY time DESC
                    LIMIT 1
                    """
                )
        except psycopg2.Error as e:
            print(f"Error fetching last stake time for job '{job_id}': {e}")
            return None

    def get_job_by_id(self, job_id: str) -> Optional[Job]:
        """
        Fetch a job by its ID from the database.

        Args:
            job_id: The ID of the job.

        Returns:
            A dictionary containing the job data, or None if the job does not exist.
        """
        conn = self.get_connector()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT id, job_type, ticker, status, params, calculate_stake, prohibit_bearish
                    FROM job
                    WHERE id = '{job_id}'
                    """
                )
                raw_job = cursor.fetchone()
                if raw_job:
                    (
                        job_id,
                        job_type,
                        ticker_name,
                        status_name,
                        parameters,
                        calculate_stake,
                        prohibit_bearish,
                    ) = raw_job
                    if not parameters:
                        parameters = {}
                    return Job(
                        id=job_id,
                        job_type=job_type,
                        ticker=Ticker[ticker_name],
                        status=JobStatus[status_name.upper()],
                        params=parameters,
                        calculate_stake=calculate_stake,
                        prohibit_bearish=prohibit_bearish,
                    )
                return None
        except psycopg2.Error as e:
            print(f"Error fetching job '{job_id}': {e}")
            return None

    def __enter__(self):
        self.get_connector()
        return self

    def __exit__(self):
        self.close_connection()

    def __del__(self):
        self.close_connection()

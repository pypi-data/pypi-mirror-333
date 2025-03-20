import hashlib
from typing import Optional

import paramiko
from paramiko import SFTPClient


class SFTPDelivery:
    """
    SFTP Delivery class to manage file uploads via SFTP.

    Attributes:
        host (str): SFTP server host.
        username (str): Username for authentication.
        password (str): Password for authentication.
        port (int): SFTP server port.
        private_key (Optional[str]): Path to the private key for key-based authentication.
        connection (paramiko.SSHClient): SSH client connection object.
        sftp_client (SFTPClient): SFTP client object.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SFTPDelivery, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = 22,
        private_key: Optional[str] = None,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key
        self.__connection = None
        self.__sftp_client = None

    @property
    def host(self) -> str:
        """
        Get the SFTP server host.

        Returns:
            str: SFTP server host.
        """
        return self.__host

    @host.setter
    def host(self, host: str) -> None:
        """
        Set the SFTP server host.

        Args:
            host (str): SFTP server host.

        Raises:
            TypeError: If 'host' is not a string.
            ValueError: If 'host' is an empty string.
        """
        if not isinstance(host, str):
            raise TypeError("'host' must be a string.")
        if not host.strip():
            raise ValueError("'host' cannot be an empty string.")
        self.__host = host

    @property
    def port(self) -> int:
        """
        Get the SFTP server port.

        Returns:
            int: SFTP server port.
        """
        return self.__port

    @port.setter
    def port(self, port: int) -> None:
        """
        Set the SFTP server port.

        Args:
            port (int): SFTP server port.

        Raises:
            TypeError: If 'port' is not an integer.
            ValueError: If 'port' is not between 1 and 65535.
        """
        if not isinstance(port, int):
            raise TypeError("'port' must be an integer.")
        if port not in range(1, 65536):
            raise ValueError("'port' must be between 1 and 65535.")
        self.__port = port

    @property
    def username(self) -> str:
        """
        Get the username for authentication.

        Returns:
            str: Username for authentication.
        """
        return self.__username

    @username.setter
    def username(self, username: str) -> None:
        """
        Set the username for authentication.

        Args:
            username (str): Username for authentication.

        Raises:
            TypeError: If 'username' is not a string.
            ValueError: If 'username' is an empty string.
        """
        if not isinstance(username, str):
            raise TypeError("'username' must be a string.")
        if not username.strip():
            raise ValueError("'username' cannot be an empty string.")
        self.__username = username

    @property
    def password(self) -> str:
        """
        Get the password for authentication.

        Returns:
            str: Password for authentication.
        """
        return self.__password

    @password.setter
    def password(self, password: str) -> None:
        """
        Set the password for authentication.

        Args:
            password (str): Password for authentication.

        Raises:
            TypeError: If 'password' is not a string.
            ValueError: If 'password' is an empty string.
        """
        if not isinstance(password, str):
            raise TypeError("'password' must be a string.")
        if not password.strip():
            raise ValueError("'password' cannot be an empty string.")
        self.__password = password

    @property
    def private_key(self) -> Optional[str]:
        """
        Get the private key path for key-based authentication.

        Returns:
            Optional[str]: Private key path.
        """
        return self.__private_key

    @private_key.setter
    def private_key(self, private_key: Optional[str]) -> None:
        """
        Set the private key path for key-based authentication.

        Args:
            private_key (Optional[str]): Path to the private key.

        Raises:
            TypeError: If 'private_key' is not a string or None.
            ValueError: If 'private_key' is an empty string.
        """
        if private_key is not None and not isinstance(private_key, str):
            raise TypeError("'private_key' must be a string or None.")
        if private_key and not private_key.strip():
            raise ValueError("'private_key' cannot be an empty string.")
        self.__private_key = private_key

    @property
    def connection(self) -> paramiko.SSHClient:
        """
        Get the SSH client connection.

        Returns:
            paramiko.SSHClient: SSH client connection.
        """
        return self.__connection

    @connection.setter
    def connection(self, connection: paramiko.SSHClient) -> None:
        """
        Set the SSH client connection.

        Args:
            connection (paramiko.SSHClient): SSH client connection.

        Raises:
            TypeError: If 'connection' is not an instance of paramiko.SSHClient.
        """
        if not isinstance(connection, paramiko.SSHClient):
            raise TypeError("'connection' must be an instance of paramiko.SSHClient.")
        self.__connection = connection

    @property
    def sftp_client(self) -> SFTPClient:
        """
        Get the SFTP client.

        Returns:
            SFTPClient: SFTP client.
        """
        return self.__sftp_client

    @sftp_client.setter
    def sftp_client(self, sftp_client: SFTPClient) -> None:
        """
        Set the SFTP client.

        Args:
            sftp_client (SFTPClient): SFTP client.

        Raises:
            TypeError: If 'sftp_client' is not an instance of SFTPClient.
        """
        if not isinstance(sftp_client, SFTPClient):
            raise TypeError("'sftp_client' must be an instance of paramiko.SFTPClient.")
        self.__sftp_client = sftp_client

    def close(self) -> None:
        """
        Close the SFTP and SSH connections.
        """
        if self.sftp_client:
            self.sftp_client.close()

        if self.connection:
            self.connection.close()

    def connect(self) -> None:
        """
        Establish a connection to the SFTP server.
        """
        self.__establish_ssh_connection()
        self.sftp_client = self.connection.open_sftp()

    def __establish_ssh_connection(self) -> None:
        """
        Establish the SSH connection based on authentication method.

        Raises:
            ValueError: If 'private_key' is set but is invalid.
        """
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.private_key:
            private_key = paramiko.RSAKey.from_private_key_file(self.private_key)
            self.connection.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                pkey=private_key,
            )
        else:
            self.connection.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
            )

    def list_files(
        self, remote_path: str = ".", pattern: str = None, names_only: bool = False
    ) -> list:
        """
        List files in a directory on the SFTP server.

        Args:
            remote_path (str): Path to the remote directory (default is current directory).
            pattern (str, optional): Pattern to filter files (e.g., '*.txt'). If None, all files are returned.
            names_only (bool): If True, only filenames are returned instead of attribute objects.

        Returns:
            list: List of file attributes or filenames if names_only is True.

        Raises:
            ValueError: If the SFTP connection is not established.
            IOError: If the remote directory doesn't exist or cannot be accessed.
        """
        if not self.sftp_client:
            raise ValueError("SFTP connection not established")

        try:
            all_files = self.sftp_client.listdir_attr(remote_path)

            if pattern:
                import fnmatch

                all_files = [
                    file
                    for file in all_files
                    if fnmatch.fnmatch(file.filename, pattern)
                ]

            if names_only:
                return [file.filename for file in all_files]
            return all_files

        except IOError as e:
            raise e

    def list_files_readable(self, remote_path: str = ".", pattern: str = None) -> list:
        """
        List files in a directory on the SFTP server with human-readable formatting.

        Args:
            remote_path (str): Path to the remote directory (default is current directory).
            pattern (str, optional): Pattern to filter files (e.g., '*.txt'). If None, all files are returned.

        Returns:
            list: List of dictionaries containing file information in a readable format.

        Raises:
            ValueError: If the SFTP connection is not established.
            IOError: If the remote directory doesn't exist or cannot be accessed.
        """
        import stat
        from datetime import datetime

        file_attrs = self.list_files(remote_path, pattern)

        readable_files = []
        for attr in file_attrs:
            mode_str = ""
            mode = attr.st_mode
            mode_str += "d" if stat.S_ISDIR(mode) else "-"
            mode_str += "r" if mode & stat.S_IRUSR else "-"
            mode_str += "w" if mode & stat.S_IWUSR else "-"
            mode_str += "x" if mode & stat.S_IXUSR else "-"
            mode_str += "r" if mode & stat.S_IRGRP else "-"
            mode_str += "w" if mode & stat.S_IWGRP else "-"
            mode_str += "x" if mode & stat.S_IXGRP else "-"
            mode_str += "r" if mode & stat.S_IROTH else "-"
            mode_str += "w" if mode & stat.S_IWOTH else "-"
            mode_str += "x" if mode & stat.S_IXOTH else "-"

            size = attr.st_size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024**2:
                size_str = f"{size/1024:.1f} KB"
            elif size < 1024**3:
                size_str = f"{size/1024**2:.1f} MB"
            else:
                size_str = f"{size/1024**3:.1f} GB"

            mtime = datetime.fromtimestamp(attr.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

            readable_files.append(
                {
                    "filename": attr.filename,
                    "size": size_str,
                    "size_bytes": attr.st_size,
                    "permissions": mode_str,
                    "modified": mtime,
                    "uid": attr.st_uid,
                    "gid": attr.st_gid,
                }
            )

        return readable_files

    def download_file(self, local_file: str, remote_file: str) -> None:
        """
        Download a file from the SFTP server.

        Args:
            remote_file (str): Path to the remote file on the server.
            local_file (str): Path to save the file locally.

        Raises:
            ValueError: If the SFTP connection is not established.
        """
        if not self.sftp_client:
            raise ValueError("SFTP connection not established")
        self.sftp_client.get(remote_file, local_file)

    def upload_file(self, local_file: str, remote_file: str) -> None:
        """
        Upload a file to the SFTP server.

        Args:
            local_file (str): Path to the local file.
            remote_file (str): Path to the remote file on the server.

        Raises:
            ValueError: If the SFTP connection is not established.
        """
        if not self.sftp_client:
            raise ValueError("SFTP connection not established")
        self.sftp_client.put(local_file, remote_file)

    def upload(self, local_file: str, remote_file: str, algorithm: str = "md5") -> bool:
        """
        Upload a file to the SFTP server and verify the upload.

        Args:
            local_file (str): Path to the local file.
            remote_file (str): Path to the remote file on the server.
            algorithm (str): The hash algorithm to use (default is 'md5').

        Returns:
            bool: True if the upload is successful and verified, False otherwise.

        Raises:
            ValueError: If the SFTP connection is not established.
        """
        if not self.sftp_client:
            raise ValueError("SFTP connection not established")

        self.upload_file(local_file, remote_file)
        return self.__verify_upload(local_file, remote_file, algorithm)

    def move_file(self, remote_source: str, remote_destination: str) -> bool:
        """
        Move a file on the SFTP server from one location to another.

        This operation is implemented as a rename operation on the remote server.

        Args:
            remote_source (str): Path to the source file on the server.
            remote_destination (str): Path to the destination file on the server.

        Returns:
            bool: True if the move operation was successful, False otherwise.

        Raises:
            ValueError: If the SFTP connection is not established.
            IOError: If the source file does not exist or cannot be accessed.
        """

        if not self.sftp_client:
            raise ValueError("SFTP connection not established")

        try:
            self.sftp_client.stat(remote_source)
            self.sftp_client.rename(remote_source, remote_destination)
            self.sftp_client.stat(remote_destination)
            return True
        except IOError:
            return False
        except FileNotFoundError:
            raise
        except Exception:
            raise

    def __calculate_checksum(self, file_path: str, algorithm: str = "md5") -> str:
        """
        Calculate the checksum of a file.

        Args:
            file_path (str): Path to the file.
            algorithm (str): The hash algorithm to use (default is 'md5').

        Returns:
            str: The checksum of the file.
        """
        hash_func = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def __verify_upload(
        self, local_file: str, remote_file: str, algorithm: str = "md5"
    ) -> bool:
        """
        Verify that the file has been uploaded correctly by comparing checksums.

        Args:
            local_file (str): Path to the local file.
            remote_file (str): Path to the remote file on the server.
            algorithm (str): The hash algorithm to use (default is 'md5').

        Returns:
            bool: True if the checksums match, False otherwise.

        Raises:
            ValueError: If the SFTP connection is not established.
        """
        if not self.sftp_client:
            raise ValueError("SFTP connection not established")

        local_checksum = self.__calculate_checksum(local_file, algorithm)

        with self.sftp_client.open(remote_file, "rb") as remote_f:
            hash_func = hashlib.new(algorithm)
            for chunk in iter(lambda: remote_f.read(4096), b""):
                hash_func.update(chunk)
            remote_checksum = hash_func.hexdigest()

        return local_checksum == remote_checksum

    def __str__(self) -> str:
        """
        Get a string representation of the SFTPDelivery instance.

        Returns:
            str: String representation of the SFTPDelivery instance.
        """
        return str(
            {
                "host": self.host,
                "port": self.port,
                "username": self.username,
                "private_key": self.private_key,
            }
        )

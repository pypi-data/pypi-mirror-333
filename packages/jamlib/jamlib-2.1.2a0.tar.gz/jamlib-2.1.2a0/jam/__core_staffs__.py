# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Dict, Literal

from jam.jwt.__tools__ import __gen_jwt__, __validate_jwt__


class AbstractConfig(ABC):
    @abstractmethod
    def __init__(
        self,
        JWT_SECRET_KEY: str | None = None,
        JWT_PRIVATE_KEY: str | None = None,
        JWT_ALGORITHM: (
            Literal[
                "HS256",
                "HS384",
                "HS512",
                "RS256",
                "RS384",
                "RS512",
                "PS256",
                "PS384",
                "PS512",
            ]
            | None  # noqa
        ) = None,
        JWT_ACCESS_EXP: int = 3600,
        JWT_REFRESH_EXP: int = 3600,
        JWT_HEADERS: dict | None = None,
    ) -> None:
        self.JWT_SECRET_KEY: str | None = JWT_SECRET_KEY
        self.JWT_PRIVATE_KEY: str | None = JWT_PRIVATE_KEY
        self.JWT_ALGORITHM: str | None = JWT_ALGORITHM

        self.JWT_ACCESS_EXP: int = JWT_ACCESS_EXP
        self.JWT_REFRESH_EXP: int = JWT_REFRESH_EXP

        if not JWT_HEADERS:
            self.JWT_HEADERS: dict = {}
        else:
            self.JWT_HEADERS: dict = JWT_HEADERS


class AbstractIntance(ABC):
    config: AbstractConfig

    @abstractmethod
    def __init__(self, config: AbstractConfig) -> None:
        self.config = config

    # @abstractmethod
    # def gen_jwt_tokens(self, **kwargs) -> Dict[str, str]:
    #     raise NotImplementedError

    @abstractmethod
    def gen_jwt_token(self, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_jwt_token(
        self, token: str, check_exp: bool, **kwargs
    ) -> Dict[str, Any]:
        raise NotImplementedError


class Config(AbstractConfig):
    """
    Base config class
    """

    def __init__(
        self,
        JWT_SECRET_KEY=None,
        JWT_PRIVATE_KEY=None,
        JWT_ALGORITHM=None,
        JWT_ACCESS_EXP=3600,
        JWT_REFRESH_EXP=3600,
        JWT_HEADERS=None,
    ):
        self.JWT_SECRET_KEY = JWT_SECRET_KEY
        self.JWT_ALGORITHM = JWT_ALGORITHM
        self.JWT_PRIVATE_KEY = JWT_PRIVATE_KEY
        self.JWT_ACCESS_EXP = JWT_ACCESS_EXP
        self.JWT_REFRESH_EXP = JWT_REFRESH_EXP
        self.JWT_HEADERS = JWT_HEADERS


class Jam(AbstractIntance):
    """
    Base Jam instance

    Args:
        config (jam.Config): jam.Config
    """

    def __init__(self, config: Config):
        super().__init__(config)

    def gen_jwt_token(self, **kwargs) -> str:
        """
        Method for generating JWT token with different algorithms.

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        """

        header = {"alg": self.config.JWT_ALGORITHM, "type": "jwt"}

        token: str = __gen_jwt__(
            header=header,
            payload=kwargs,
            secret=self.config.JWT_SECRET_KEY,
            private_key=self.config.JWT_PRIVATE_KEY,
        )

        return token

    def decode_jwt_token(
        self, token: str, check_exp: bool = False, **kwargs
    ) -> Dict[str, Any]:
        """
        Validate a JWT token and return the payload if valid.

        Args:
            token (str): The JWT token to validate.
            check_exp (bool): true to check token lifetime.
            secret (str | None): Secret key for HMAC algorithms.
            public_key (str | None): Public key for RSA algorithms.

        Returns:
            (Dict[str, Any]): The payload if the token is valid.

        Raises:
            ValueError: If the token is invalid.
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
            EmtpyPublicKey: If RSA algorithm is selected, but public key None.
            NotFoundSomeInPayload: If 'exp' not found in payload.
            TokenLifeTimeExpired: If token has expired.
        """

        payload = __validate_jwt__(
            token=token,
            check_exp=check_exp,
            secret=kwargs["secret"],
            public_key=kwargs["public_key"],
        )

        return payload

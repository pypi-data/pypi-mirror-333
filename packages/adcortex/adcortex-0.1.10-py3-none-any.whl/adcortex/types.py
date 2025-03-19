"""Types for ADCortex API.

This module defines data classes and enumerations used by the ADCortex API client.
"""

from pydantic import BaseModel, validator
from typing import List, Dict, Any
from enum import Enum
import pycountry


class Gender(str, Enum):
    """
    Gender enumeration.

    Attributes:
        male: Represents the male gender.
        female: Represents the female gender.
        other: Represents any gender not covered by male or female.
    """

    male = "male"
    female = "female"
    other = "other"


class Role(str, Enum):
    """
    Role enumeration.

    Attributes:
        user: Indicates that the message sender is a user.
        ai: Indicates that the message sender is an AI.
    """

    user = "user"
    ai = "ai"


class Interest(str, Enum):
    """
    Interest enumeration.

    Attributes:
        flirting: Indicates an interest in flirting.
        gaming: Indicates an interest in gaming.
        sports: Indicates an interest in sports.
        music: Indicates an interest in music.
        travel: Indicates an interest in travel.
        technology: Indicates an interest in technology.
        art: Indicates an interest in art.
        cooking: Indicates an interest in cooking.
        all: Represents all interests.
    """

    flirting = "flirting"
    gaming = "gaming"
    sports = "sports"
    music = "music"
    travel = "travel"
    technology = "technology"
    art = "art"
    cooking = "cooking"
    all = "all"  # Option for all interests


class UserInfo(BaseModel):
    """
    Stores user information for ADCortex API.

    Attributes:
        user_id (str): Unique identifier for the user.
        age (int): User's age.
        gender (Gender): User's gender.
        location (str): User's location (ISO 3166-1 alpha-2 code).
        language (str): Preferred language (must be "english").
        interests (List[Interest]): A list of user's interests.
    """

    user_id: str
    age: int
    gender: Gender
    location: str  # Stored as ISO code.
    language: str = "en"  # Default to "english"
    interests: List[Interest]

    @validator("location")
    def validate_country(cls, value):
        """
        Validate that the provided country code is a valid ISO 3166-1 alpha-2 code.
        """
        if value not in [country.alpha_2 for country in pycountry.countries]:
            raise ValueError(f"{value} is not a valid country code.")
        return value

    @validator("language")
    def validate_language(cls, value):
        """
        Validate that the provided language code is "english".
        """
        if value.lower() != "en":
            raise ValueError("Language must be 'english'.")
        return value


class Platform(BaseModel):
    """
    Contains platform-related metadata.

    Attributes:
        name (str): Name of the platform.
        version (str): Version of the platform.
    """

    name: str
    version: str


class SessionInfo(BaseModel):
    """
    Stores session details including user and platform information.

    Attributes:
        session_id (str): Unique identifier for the session.
        character_name (str): Name of the character (assistant).
        character_metadata (Dict[str, Any]): Additional metadata for the character.
        user_info (UserInfo): User information.
        platform (Platform): Platform details.
    """

    session_id: str
    character_name: str
    character_metadata: Dict[str, Any] = {"description": ""}
    user_info: UserInfo
    platform: Platform


class Message(BaseModel):
    """
    Represents a single message in a conversation.

    Attributes:
        role (Role): The role of the message sender (either user or AI).
        content (str): The content of the message.
    """

    role: Role
    content: str


class Ad(BaseModel):
    """
    Represents an advertisement fetched via the ADCortex API.

    Attributes:
        idx (int): Identifier for the advertisement.
        ad_title (str): Title of the advertisement.
        ad_description (str): Description of the advertisement.
        placement_template (str): Template used for ad placement.
        link (str): URL link to the advertised product or service.
    """

    idx: int
    ad_title: str
    ad_description: str
    placement_template: str
    link: str

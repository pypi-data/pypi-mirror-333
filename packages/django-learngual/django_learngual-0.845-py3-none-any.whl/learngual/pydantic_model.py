from typing import Literal

from pydantic import AnyHttpUrl, Field

from .interface import BaseModel, BaseTypeModel


class SocialMediaLinksSchema(BaseModel):
    facebook: AnyHttpUrl | None = Field(None)
    instagram: AnyHttpUrl | None = Field(None)
    linkedin: AnyHttpUrl | None = Field(None)
    twitter: AnyHttpUrl | None = Field(None)
    website: AnyHttpUrl | None = Field(None)


"""
Account settings link
"""


class AccountSettingsSchema:
    class Base(BaseTypeModel):
        type: Literal["DEFAULT"] = "DEFAULT"
        social_links: SocialMediaLinksSchema = Field(
            default_factory=SocialMediaLinksSchema
        )

    class EnterpriseSettings(Base, BaseTypeModel):

        type: Literal["ENTERPRISE"] = "ENTERPRISE"
        who_can_view_your_profile: Literal[
            "Enterprise members only",
            "Enterprise members and public viewers",
            "Public viewers",
        ] = Field("Enterprise members only")
        show_statistics: bool = Field(False)
        show_available_course_languages: bool = Field(False)
        show_social_media_links: bool = Field(False)
        show_courses: bool = Field(False)

    class InstructorSettings(Base):
        type: Literal["INSTRUCTOR"] = "INSTRUCTOR"
        who_can_view_your_profile: Literal[
            "Students only",
            "Instructors only",
            "Students and instructors",
            "All enterprise",
        ] = Field("Friends")
        show_statistics: bool = Field(True)
        show_available_course_languages: bool = Field(True)
        show_social_media_links: bool = Field(True)
        show_courses: bool = Field(True)
        show_affiliates: bool = Field(True)

    class PersonalSettings(Base):
        who_can_view_your_profile: Literal[
            "Friends",
            "All affiliated accounts",
            "Public",
            "Students and enterprise",
            "Students and instructors",
        ] = Field("Friends")
        show_evaluations: bool = Field(True)
        show_achievements: bool = Field(True)
        show_affiliate: bool = Field(True)
        show_courses: bool = Field(True)
        exercises_per_week: int = Field(0)

        type: Literal["PERSONAL"] = "PERSONAL"

    class DeveloperSettings(Base):
        type: Literal["DEVELOPER"] = "DEVELOPER"

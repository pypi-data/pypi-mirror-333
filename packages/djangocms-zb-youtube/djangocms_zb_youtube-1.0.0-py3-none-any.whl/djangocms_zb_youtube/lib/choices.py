# -*- coding: utf-8 -*-

#      Copyright (C)  2022. CQ Inversiones SAS.
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

# ********************************************************
# Project: django_cms
# IDE: PyCharm
# Developed by: macercha
# File Name: choices.py
# Date: 18/02/22 - 8:02 AM
# *******************************************************
from django.utils.translation import gettext_lazy as _


class YoutubeOrderChoices:
    """
    Choices for Youtube Order Options
    """
    DATE = "date"
    RATING = "rating"
    RELEVANCE = "relevance"
    TITLE = "title"
    VIDEO_COUNT = "videoCount"
    VIEW_COUNT = "viewCount"

    ORDER_CHOICES = (
        (DATE, _("Date")),
        (RATING, _("Rating")),
        (RELEVANCE, _("Relevance")),
        (TITLE, _("Title")),
        (VIDEO_COUNT, _("Video Count")),
        (VIEW_COUNT, _("View Count"))
    )


class YoutubeThumbnailDefinitions:
    """
    Choices for Thumbnail Definitions
    """
    LOW = "default"
    MEDIUM = "medium"
    HIGH = "high"

    THUMBNAILS_DEFINITION = (
        (LOW, _("Low")),
        (MEDIUM, _("Medium")),
        (HIGH, _("High"))
    )


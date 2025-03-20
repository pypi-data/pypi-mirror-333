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

from cms.models.pluginmodel import CMSPlugin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangocms_zb_youtube.lib.choices import YoutubeOrderChoices
from djangocms_zb_youtube.lib.choices import YoutubeThumbnailDefinitions


class PluginConfig(CMSPlugin):
    """
    CMSPlugin ZbYoutube entity
    """
    channel_id = models.CharField(null=False, blank=True, default="", max_length=100, verbose_name=_("Channel Id"),
                                  help_text=_("Youtube channel id to view"))
    playlist_id = models.CharField(null=False, blank=True, default="", max_length=100, verbose_name=_("Playlist Id"),
                                   help_text=_("Playlist id to view"))
    max_results = models.IntegerField(null=False, blank=False, default=4, verbose_name=_("Max results"),
                                      help_text=_("Max number of videos to be fetched from Youtube"))
    video_order = models.CharField(null=False, blank=False, choices=YoutubeOrderChoices.ORDER_CHOICES,
                                   default=YoutubeOrderChoices.DATE, max_length=10, verbose_name=_("Video order"),
                                   help_text=_("Order in which videos are displayed"))
    video_template = models.CharField(max_length=50, null=False, blank=False, default="zb_youtube.html",
                                      verbose_name=_("Template"),
                                      help_text=_("Template to be used to display the videos"))
    video_width = models.IntegerField(null=False, default=560, verbose_name=_("Video width"),
                                      help_text=_("Width of video in pixels"))
    video_height = models.IntegerField(null=False, default=315, verbose_name=_("Video height"),
                                       help_text=_("Height of video in pixels"))
    video_columns = models.IntegerField(null=False, default=2, verbose_name=_("Display columns"),
                                        help_text=_("Number of columns in which the videos will be displayed"))
    thumbnail_definition = models.CharField(max_length=10, null=False, blank=False,
                                            choices=YoutubeThumbnailDefinitions.THUMBNAILS_DEFINITION,
                                            default=YoutubeThumbnailDefinitions.MEDIUM,
                                            verbose_name=_("Thumbnail definition"),
                                            help_text=_("Definition of thumbnail to be used"))
    refresh_time = models.IntegerField(default=360, null=False, blank=False,
                                       validators=[MinValueValidator(60), MaxValueValidator(1440)],
                                       verbose_name=_("Refresh time"),
                                       help_text=_("Time to be used to refresh the video list from youtube"))

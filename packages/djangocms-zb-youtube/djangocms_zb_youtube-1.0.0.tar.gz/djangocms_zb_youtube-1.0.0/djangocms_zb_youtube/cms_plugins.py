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
# File Name: cms_plugins.py
# Date: 18/02/22 - 7:59 AM
# *******************************************************
import os.path
import requests
from datetime import datetime
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djangocms_zb_youtube.models import PluginConfig


@plugin_pool.register_plugin
class DjangocmsZbYoutubePlugin(CMSPluginBase):
    """
    Youtube Plugin Class for DjangoCMS
    Use ZB_YOUTUBE_API_KEY for request
    """
    name = _("Django CMS Zibanu Youtube Connector")
    module = "Zibanu"
    model = PluginConfig
    cache = False
    # *****************************************************************************
    # COMMENT: Add evaluation of ZB_CMS_YOUTUBE_API_KEY for run the plugin.
    # Modified by: macercha
    # Modified at: 2025-03-13, 18:59
    # *****************************************************************************
    if hasattr(settings, 'ZB_CMS_YOUTUBE_API_KEY'):
        api_key = settings.ZB_CMS_YOUTUBE_API_KEY
    elif hasattr(settings, 'ZB_YOUTUBE_API_KEY'):
        api_key = settings.ZB_YOUTUBE_API_KEY
    else:
        raise ImproperlyConfigured(_("ZB_CMS_YOUTUBE_API_KEY or ZB_YOUTUBE_API_KEY not set."))

    if not api_key:
        raise ImproperlyConfigured(_("ZB_CMS_YOUTUBE_API_KEY or ZB_YOUTUBE_API_KEY not set."))

    def __get_url(self, instance) -> tuple:
        """
        Get url string to query videos from Channel Id or Playlist Id
        :param channel_id: str: Youtube channel id
        :param playlist_id: str: Playlist id
        :return: str: url to query
        """
        url = ""
        query_type = 0
        if len(instance.channel_id) > 0:
            url = "https://www.googleapis.com/youtube/v3/search?"
            url += "key=" + self.api_key + "&channelId=" + instance.channel_id
            url += "&part=snippet,id&order=" + instance.video_order
            url += "&maxResults=" + str(instance.max_results)
            url += "&type=video"
            query_type = 0
        elif len(instance.playlist_id) > 0:
            url = "https://www.googleapis.com/youtube/v3/playlistItems?"
            url += "key=" + self.api_key + "&playlistId=" + instance.playlist_id
            url += "&part=snippet,id&maxResults=" + str(instance.max_results)
            url += "&order=" + instance.video_order + "&type=video"
            query_type = 1

        return url, query_type

    def __load_request(self, instance) -> list:
        """
        Method to load json from youtube request API
        :param context: Context of plugin
        :param instance: Model instance for data access
        :return: list: video_list with json structures from youtube

        """
        video_list = []
        try:
            """
            Force get of video list from youtube.
            """
            url, query_type = self.__get_url(instance)
            response = requests.get(url, timeout=3)

            if response.status_code == 200:
                json_response = response.json()["items"]
            else:
                json_response = []

            for item in json_response:
                snippet = item.get("snippet")
                video_list.append(
                    {
                        "video_id": item.get("id").get("videoId") if query_type == 0 else snippet.get("resourceId").get("videoId"),
                        "published_at": datetime.fromisoformat(
                            item.get("snippet").get("publishedAt", timezone.now())[:-1] + "+00:00").strftime(
                            "%Y-%m-%d %H:%M"),
                        "title": snippet.get("title", ""),
                        "description": snippet.get("description", ""),
                        "thumbnail": snippet.get("thumbnails").get(instance.thumbnail_definition)
                    }
                )
        except Exception as err:
            video_list = []
        finally:
            return video_list

    def __load_videos(self, context, instance):
        """
        Method to load videos from cache or request ton youtube.
        :param context: context of plugin
        :param instance: instance of plugin
        :return: JSON:
            json_return =  {
                "video_width": Width to iframe of video
                "video_height": Height to iframe of video
                "video_columns": Columns to be displayed of videos
                "videos": Json array with video data
                    "video_id": Video ID of Youtube
                    "published_at": Date time of published
                    "title": Video Title
                    "description": Video description
                    "thumbnail": Thumbnail structure
                        "url": URL of thumbnail image
                        "width": Width of thumbnail image
                        "height" Height of thumbnail image
            }
        """
        cache_name = "zb_youtube_" + self.api_key + "_" + str(instance.cmsplugin_ptr_id)
        json_youtube = cache.get(cache_name)
        is_edit_mode = False
        force_load = False

        # Define if is in edit_mode
        try:
            parent_request = context.dicts[1].get("request")
            is_edit_mode = parent_request.toolbar.edit_mode_active
        except:
            pass

        if json_youtube is None or is_edit_mode:
            # Define json_return
            json_youtube = {
                "video_width": instance.video_width,
                "video_height": instance.video_height,
                "video_columns": instance.video_columns,
                "last_query": None,
                "videos": []
            }

        # Evaluate cache age
        if json_youtube.get("last_query", None) is None:
            force_load = True
        else:
            if int((timezone.now() - json_youtube.get("last_query")).total_seconds()/60) > instance.refresh_time:
                force_load = True

        if force_load:
            cache.delete(cache_name)
            video_list = self.__load_request(instance)
            if len(video_list) > 0:
                json_youtube["videos"] = video_list.copy()
                json_youtube["last_query"] = timezone.now()
            cache.set(cache_name, json_youtube, instance.refresh_time * 60)
        return json_youtube

    def _get_render_template(self, context, instance, placeholder):
        """
        Private method to replace default template in CMS
        :param context: Context CMS Var
        :param instance: Model instance
        :param placeholder: Placeholder
        :return: str: Name of new template
        """
        base_dir = "djangocms_zb_youtube"
        base_template = "zb_youtube.html"
        if instance.video_template:
            base_template = instance.video_template

        return os.path.join(base_dir, base_template)

    def get_render_template(self, context, instance, placeholder):
        """
        Method required for djangocms
        :param context: Contexto of plugins
        :param instance: Instance of PluginModel
        :param placeholder: Placeholder of template
        :return: Render template
        """
        return self._get_render_template(context, instance, placeholder)

    def render(self, context, instance, placeholder):
        """
        Override method to render template
        :param context: Context CMS Var
        :param instance: Model instance
        :param placeholder: Placeholder
        :return: context
        """
        json_youtube = self.__load_videos(context, instance)
        context = super().render(context, instance, placeholder)
        context.update({
            "youtube_info": json_youtube
        })
        return context

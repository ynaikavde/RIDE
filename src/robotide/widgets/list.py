#  Copyright 2008-2011 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

IS_WINDOWS = os.sep == '\\'


class VirtualList(wx.ListCtrl, ListCtrlAutoWidthMixin):
    _style = wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_HRULES|wx.LC_VIRTUAL

    def __init__(self, parent, headers, model):
        wx.ListCtrl.__init__(self, parent, style=self._style)
        ListCtrlAutoWidthMixin.__init__(self)
        self._model = model
        self._selection_listeners = []
        self._create_headers(headers)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        if IS_WINDOWS:
            self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.SetItemCount(model.count)
        self.SetImageList(model.images, wx.IMAGE_LIST_SMALL)


    def OnLeftDown(self, event):
        item, flags =  self.HitTest(event.Position)
        if flags | wx.LIST_HITTEST_ONITEM:
            wx.CallAfter(self._force_item_selection, item)
        event.Skip()

    def _force_item_selection(self, item):
        # On Windows, wx.EVT_LIST_ITEM_SELECTED is not generated when
        # already selected item is selected again.
        self.Select(item, False)
        self.Select(item, True)

    def _create_headers(self, headers):
        for idx, name in enumerate(headers):
            self.InsertColumn(idx, name)
        self.SetColumnWidth(0, 200)
        self.SetColumnWidth(1, 160)

    def refresh(self):
        self.SetItemCount(self._model.count)
        self.SetImageList(self._model.images, wx.IMAGE_LIST_SMALL)

    def add_selection_listener(self, listener):
        self._selection_listeners.append(listener)

    def OnListItemSelected(self, event):
        for listener in self._selection_listeners:
            listener(event.Index)

    def OnGetItemText(self, row, col):
        return self._model.item_text(row, col)

    def OnGetItemImage(self, item):
        return self._model.image(item)

    def OnGetItemAttr(self, item):
        return self._model.item_attributes(item)


class ListModel(object):

    @property
    def count(self):
        return 0

    @property
    def images(self):
        return None

    def item_text(self, row, col):
        return ''

    def image(self, row):
        return None

    def item_attributes(self, row):
        return None


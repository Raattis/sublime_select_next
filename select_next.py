import sublime
import sublime_plugin
import re

selection_added = False
added_selections = []

def trace(*args, **kwargs):
  print(*args, **kwargs)
  pass

class SelectNext(sublime_plugin.TextCommand):
  def __init__(self, view):
    super().__init__(view)
    self.last_word = None

  def run(self, edit, word = False, backward = False, skip = False, undo_last_selection = False, clear_selections = False):
    trace("run start (",word,")")
    if clear_selections:
      if len(added_selections) > 0:
        p = added_selections[0].b
        added_selections.clear()
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(p, p))
      elif len(self.view.sel()) > 0:
        region = self.view.sel()[0]
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(region.b, region.b))
      return


    if undo_last_selection:
      self.remove_last_selection()
      return

    self.last_word = word
    self.last_backward = backward

    sels = self.view.sel()
    if len(sels) == 0:
      return

    result = self._get_next_selection(sels, word, backward)
    trace(result)
    if result == None:
      return

    sel, matches, shift = result
    self._append_selection(sel, matches, shift)

    global selection_added
    selection_added = True
    trace("added_selections:", added_selections, "")
    trace("run end")

  def _append_selection(self, sel, matches, shift):
    try:
      match = matches.__next__()
    except StopIteration:
      return

    start, end = match.start(1) + shift, match.end(1) + shift
    if sel.a > sel.b:
      start, end = end, start

    selection = sublime.Region(start, end)

    added_selections.insert(0, selection)
    self.view.sel().clear()
    self.view.sel().add_all(added_selections)
    self.view.show(selection)

    regions = []
    for match in matches:
      start, end = match.start(1) + shift, match.end(1) + shift
      region = sublime.Region(start, end)
      regions.append(region)


    self.view.erase_regions('select_region')
    self.view.add_regions('select_region', regions, 'string', '',
      sublime.DRAW_EMPTY)

  def remove_last_selection(self):
    if len(added_selections) <= 1:
      if len(added_selections) == 1:
        p = added_selections[0].b;
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(p, p))
      elif len(self.view.sel()) == 0:
        self.view.sel().add(sublime.Region(0, 0))
      self.view.show(self.view.sel()[0])
      added_selections.clear()
      return

    added_selections.pop(0)
    self.view.sel().clear()
    self.view.sel().add_all(added_selections)
    self.view.show(added_selections[0])

  def _get_next_selection(self, sels, word, backward):
    if backward:
      sel = sels[0]
    else:
      sel = sels[-1]

    if sel.empty():
      sel = self.view.word(sel.b)
      if sel.empty():
        return None
      if backward:
        cursor = sel.end()
      else:
        cursor = sel.begin()
    else:
      if backward:
        cursor = sel.begin()
      else:
        cursor = sel.end()

    selected = self.view.substr(sel)
    if backward:
      region = sublime.Region(0, cursor)
    else:
      region = sublime.Region(cursor, self.view.size())

    text = self.view.substr(region)

    if word:
      matches = re.finditer(r'\W(' + re.escape(selected) + r')\W', text)
      #matches = re.finditer(r'(' + re.escape(selected) + r')', text)
    else:
      matches = re.finditer(r'(' + re.escape(selected) + r')', text)

    if backward:
      matches = reversed(list(matches))

    return sel, matches, region.a

class SelectNextListener(sublime_plugin.EventListener):
  def on_selection_modified_async(self, view):
    global selection_added
    if selection_added:
      selection_added = False
      trace("ignoring on_selection_modified_async")
      return

    sels = view.sel()
    for sel in sels:
      if (not sel.empty() or len(sels) > 1) and not sel in added_selections:
        trace("missing sel added:", sel)
        added_selections.insert(0, sel)

    for i in range(len(added_selections) - 1, -1, -1):
      sel = added_selections[i]
      if not sel in sels:
        trace("false sel removed:", sel)
        del added_selections[i]

    trace("handler - added_selections:", added_selections, ", view:", view)

    view.erase_regions('select_next')
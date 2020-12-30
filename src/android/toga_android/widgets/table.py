from travertino.size import at_least

from ..libs import android_widgets
from .base import Widget
from toga_android.window import AndroidViewport


class TogaOnClickListener(android_widgets.OnClickListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onClick(self, _view):
        tr_id = _view.getId()
        print('tr_id='+str(tr_id))
        row = self.impl.interface.data[tr_id]
        if self.impl.interface.multiple_select:
            if tr_id in self.impl.selection:
                self.impl.selection.pop(tr_id)
                _view.setBackgroundColor(-1)  # WHITE, this should not be hard-coded, but what better way?
            else:
                self.impl.selection[tr_id] = row
                _view.setBackgroundColor(-3355444)  # LTGREY, this should not be hard-coded, but what better way?
        else:
            self.impl.clear_selection()
            self.impl.selection[tr_id] = row
            _view.setBackgroundColor(-3355444)  # LTGREY, this should not be hard-coded, but what better way?
        print('selection='+str(self.impl.selection))
        if self.impl.interface.on_select:
            self.impl.interface.on_select(self.impl.interface, row=row)


class Table(Widget):
    table_layout = None
    selection = {}

    def create(self):
        self.table_layout = android_widgets.TableLayout(self._native_activity)
        table_layout_params = android_widgets.TableLayout__Layoutparams(
            android_widgets.TableLayout__Layoutparams.MATCH_PARENT,
            android_widgets.TableLayout__Layoutparams.WRAP_CONTENT
        )
        self.table_layout.setLayoutParams(table_layout_params)
        self.native = self.table_layout
        #widget.viewport = AndroidViewport(widget.native)
        if self.interface.data is not None:
            self.change_source(self.interface.data)

    def change_source(self, source):
        print('change_source: '+str(source))
        print('# of rows: '+str(len(source)))
        self.selection = {}
        if source is None:
            return
        self.table_layout.removeAllViews()
        self.table_layout.addView(self.create_table_header())
        for row_index in range(len(source)):
            table_row = self.create_table_row(row_index)
            self.table_layout.addView(table_row)

    def clear_selection(self):
        for i in range(self.table_layout.getChildCount()):
            row = self.table_layout.getChildAt(i)
            row.setBackgroundColor(-1)  # WHITE, this should not be hard-coded, but what better way?
        self.selection = {}

    def create_table_header(self):
        table_row = android_widgets.TableRow(self._native_activity)
        table_row_params = android_widgets.TableRow__Layoutparams(
            android_widgets.TableRow__Layoutparams.MATCH_PARENT,
            android_widgets.TableRow__Layoutparams.WRAP_CONTENT
        )
        table_row.setLayoutParams(table_row_params)
        for col_index in range(len(self.interface._accessors)):
            text_view = android_widgets.TextView(self._native_activity)
            text_view.setText(self.interface.headings[col_index])
            text_view_params = android_widgets.TableRow__Layoutparams(
                android_widgets.TableRow__Layoutparams.MATCH_PARENT,
                android_widgets.TableRow__Layoutparams.WRAP_CONTENT
            )
            text_view_params.setMargins(10, 5, 10, 5)  # left, top, right, bottom
            text_view_params.gravity = android_widgets.Gravity.START
            text_view.setLayoutParams(text_view_params)
            table_row.addView(text_view)
        return table_row

    def create_table_row(self, row_index):
        table_row = android_widgets.TableRow(self._native_activity)
        table_row_params = android_widgets.TableRow__Layoutparams(
            android_widgets.TableRow__Layoutparams.MATCH_PARENT,
            android_widgets.TableRow__Layoutparams.WRAP_CONTENT
        )
        table_row.setLayoutParams(table_row_params)
        table_row.setClickable(True)
        table_row.setOnClickListener(TogaOnClickListener(impl=self))
        table_row.setId(row_index)
        for col_index in range(len(self.interface._accessors)):
            text_view = android_widgets.TextView(self._native_activity)
            text_view.setText(self.get_data_value(row_index, col_index))
            text_view_params = android_widgets.TableRow__Layoutparams(
                android_widgets.TableRow__Layoutparams.MATCH_PARENT,
                android_widgets.TableRow__Layoutparams.WRAP_CONTENT
            )
            text_view_params.setMargins(10, 5, 10, 5)  # left, top, right, bottom
            text_view_params.gravity = android_widgets.Gravity.START
            text_view.setLayoutParams(text_view_params)
            table_row.addView(text_view)
        return table_row

    def get_data_value(self, row_index, col_index):
        if self.interface.data is None or self.interface._accessors is None:
            return None
        row_object = self.interface.data[row_index]
        value = getattr(row_object, self.interface._accessors[col_index])
        #print('data({},{})={}'.format(row_index, col_index, value))
        return value

    def get_selection(self):
        _selection = []
        for row_index in range(len(self.interface.data)):
            if row_index in self.selection:
                _selection.append(self.selection[row_index])
        if len(_selection) == 0:
            _selection = None
        elif not self.interface.multiple_select:
            _selection = _selection[0]
        return _selection

    def scroll_to_row(self, row):
        pass

    def set_on_select(self, _on_select):
        self.interface.factory.not_implemented('Table.set_on_select()')

    def set_on_double_click(self, _on_double_click):
        self.interface.factory.not_implemented('Table.set_on_double_click()')

    def add_column(self, heading, accessor):
        self.change_source(self.interface.data)

    def remove_column(self, accessor):
        self.change_source(self.interface.data)

    def rehint(self):
        # Android can crash when rendering some widgets until they have their layout params set. Guard for that case.
        if self.native.getLayoutParams() is None:
            return
        self.native.measure(
            android_widgets.View__MeasureSpec.UNSPECIFIED,
            android_widgets.View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()

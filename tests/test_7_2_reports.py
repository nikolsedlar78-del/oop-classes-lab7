import pytest
from lab7.reports import Report, SalesReport, InventoryReport


def test_report_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Report()


def test_sales_report_build():
    r = SalesReport({"apple": 10, "pear": 5.5})
    assert r.build() == "Sales report\napple: 10.00\npear: 5.50\nTotal: 15.50"


def test_sales_report_empty():
    assert SalesReport({}).build() == "Sales report\nTotal: 0.00"


def test_sales_zero_amount_boundary():
    assert SalesReport({"free": 0}).build() == "Sales report\nfree: 0.00\nTotal: 0.00"


def test_inventory_report_default_footer():
    r = InventoryReport({"bolt": 100, "nut": 0})
    assert r.build() == "Inventory report\nbolt: 100 pcs\nnut: 0 pcs\n-- end of report --"


def test_inventory_empty():
    assert InventoryReport({}).build() == "Inventory report\n-- end of report --"


def test_inventory_uses_base_footer():
    assert InventoryReport({}).footer() == Report.footer(InventoryReport({}))


def test_template_order_header_rows_footer():
    class Custom(Report):
        def header(self):
            return "H"
        def rows(self):
            return ["r1", "r2"]
        def footer(self):
            return "F"
    assert Custom().build() == "H\nr1\nr2\nF"


def test_subclass_must_implement_abstract_steps():
    class NoRows(Report):
        def header(self):
            return "H"
    with pytest.raises(TypeError):
        NoRows()


@pytest.mark.parametrize("cls,data", [(SalesReport, {"a": 1}), (InventoryReport, {"a": 1})])
def test_isinstance_report(cls, data):
    assert isinstance(cls(data), Report)


def test_report_does_not_share_state_with_source_dict():
    src = {"a": 1}
    r = SalesReport(src)
    src["b"] = 2
    assert "b" not in r.build()


@pytest.mark.parametrize("bad", [None, [("a", 1)], "a"])
def test_non_dict_input(bad):
    with pytest.raises(TypeError):
        SalesReport(bad)
    with pytest.raises(TypeError):
        InventoryReport(bad)


def test_invalid_values():
    with pytest.raises(ValueError):
        SalesReport({"a": -1})
    with pytest.raises(ValueError):
        SalesReport({"": 1})
    with pytest.raises(ValueError):
        InventoryReport({"a": 1.5})
    with pytest.raises(ValueError):
        InventoryReport({"a": -1})

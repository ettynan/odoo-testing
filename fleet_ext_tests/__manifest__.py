{
    "name": "Fleet External Tests",
    "summary": "Unit tests for Odoo Fleet (external addon)",
    "version": "15.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["fleet"],    # <- key line: we rely on Fleet
    "installable": True,
    "application": False,
}

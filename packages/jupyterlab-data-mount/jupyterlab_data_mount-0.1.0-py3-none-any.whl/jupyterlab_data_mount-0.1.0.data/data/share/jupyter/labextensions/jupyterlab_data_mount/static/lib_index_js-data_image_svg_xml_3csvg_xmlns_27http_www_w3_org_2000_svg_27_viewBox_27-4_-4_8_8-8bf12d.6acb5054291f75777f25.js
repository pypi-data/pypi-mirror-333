"use strict";
(self["webpackChunkjupyterlab_data_mount"] = self["webpackChunkjupyterlab_data_mount"] || []).push([["lib_index_js-data_image_svg_xml_3csvg_xmlns_27http_www_w3_org_2000_svg_27_viewBox_27-4_-4_8_8-8bf12d"],{

/***/ "./lib/commands.js":
/*!*************************!*\
  !*** ./lib/commands.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CommandIDs: () => (/* binding */ CommandIDs),
/* harmony export */   addCommands: () => (/* binding */ addCommands)
/* harmony export */ });
/* harmony import */ var _dialog_widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./dialog/widget */ "./lib/dialog/widget.js");
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./icon */ "./lib/icon.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");




var CommandIDs;
(function (CommandIDs) {
    CommandIDs.opendialog = 'jupyterlab-data-mount:opendialog';
})(CommandIDs || (CommandIDs = {}));
function addCommands(app, sbwidget, templates, mountDir) {
    app.commands.addCommand(CommandIDs.opendialog, {
        label: args => 'Open Data Mount',
        caption: 'Open Data Mount',
        icon: args => _icon__WEBPACK_IMPORTED_MODULE_1__.cloudStorageIcon,
        execute: async () => {
            const buttons = [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: 'Cancel' }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Mount' })
            ];
            const body = new _dialog_widget__WEBPACK_IMPORTED_MODULE_2__.MountDialogBody(true, {}, templates, mountDir);
            body.node.style.overflow = 'visible';
            body.node.className = 'data-mount-dialog-body';
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Data Mount',
                body: body,
                buttons: buttons
            }).then(result => {
                if (result.button.accept) {
                    handleResult(result.value, sbwidget, mountDir);
                }
            });
        }
    });
}
async function handleResult(result, sbwidget, mountDir) {
    try {
        result.loading = true;
        sbwidget.addMountPoint(result);
        await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.RequestAddMountPoint)(result);
        result.loading = false;
        sbwidget.setMountPointLoaded(result);
    }
    catch (reason) {
        alert(`Could not mount ${result.options.displayName}.\nCheck ${mountDir}/mount.log for details`);
        await sbwidget.removeMountPoint(result, true);
    }
}


/***/ }),

/***/ "./lib/components/checkbox.js":
/*!************************************!*\
  !*** ./lib/components/checkbox.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ Checkbox)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-tooltip */ "webpack/sharing/consume/default/react-tooltip/react-tooltip");
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_tooltip__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_material_Checkbox__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/Checkbox */ "./node_modules/@mui/material/Checkbox/Checkbox.js");



class Checkbox extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.state = {
            checked: props.checked || true
        };
        // Bind the methods to the instance
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
        const checked = event.target.checked;
        this.setState({ checked });
        if (this.props.onChange) {
            this.props.onChange(event);
        }
    }
    // Method to get the current value of the text input
    getValue() {
        return this.state.checked;
    }
    render() {
        const { label, name, checked, tooltip } = this.props;
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "row" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "col-12" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "row mb-1" },
                    label && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "col-4 col-form-label d-flex align-items-center" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", null,
                            label,
                            ":"),
                        tooltip && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { "data-tooltip-id": `data-mount-tooltip-${name}`, "data-tooltip-html": tooltip, "data-tooltip-place": "top", className: "lh-1 ms-auto data-mount-dialog-label-tooltip" },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { xmlns: "http://www.w3.org/2000/svg", width: "16", height: "16", fill: "currentColor", className: "bi bi-info-circle", viewBox: "0 0 16 16", style: { verticalAlign: 'sub' } },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" }),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z" })))))),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "col-8 d-flex flex-column justify-content-center" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "input-group" },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Checkbox__WEBPACK_IMPORTED_MODULE_2__["default"], { name: name, checked: checked, onChange: this.handleChange, inputProps: { 'aria-label': 'controlled' }, disabled: !this.props.editable }))))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_tooltip__WEBPACK_IMPORTED_MODULE_1__.Tooltip, { id: `data-mount-tooltip-${name}` })));
    }
}


/***/ }),

/***/ "./lib/components/dropdown.js":
/*!************************************!*\
  !*** ./lib/components/dropdown.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DropdownComponent: () => (/* binding */ DropdownComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_select__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-select */ "webpack/sharing/consume/default/react-select/react-select");
/* harmony import */ var react_select__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_select__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-tooltip */ "webpack/sharing/consume/default/react-tooltip/react-tooltip");
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_tooltip__WEBPACK_IMPORTED_MODULE_2__);



class DropdownComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.handleChange = (event) => {
            this.props.onValueChange(this.props.key_, event.target.value);
        };
        this.handleSearchableChange = (event) => {
            this.props.onValueChange(this.props.key_, event.value);
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSearchableChange = this.handleSearchableChange.bind(this);
        this.selectRef = react__WEBPACK_IMPORTED_MODULE_0__.createRef();
    }
    render() {
        const selected = this.props.selected;
        const values = this.props.values;
        const label = this.props.label;
        const tooltip = this.props.tooltip;
        let valuesReact;
        valuesReact = values.map(x => {
            if (x.value === selected) {
                return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { value: x.value, selected: true }, x.label));
            }
            else {
                return react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { value: x.value }, x.label);
            }
        });
        // <div className="lm-Widget p-Widget jp-Dialog-body" style={{ overflow: 'visible' }}>
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "row" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "col-12" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "row mb-1" },
                    label && (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "col-4 col-form-label d-flex align-items-center" },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("label", null,
                            label,
                            ":"),
                        tooltip && (react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { "data-tooltip-id": `data-mount-tooltip-${name}`, "data-tooltip-html": tooltip, "data-tooltip-place": "top", className: "lh-1 ms-auto data-mount-dialog-label-tooltip" },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", { xmlns: "http://www.w3.org/2000/svg", width: "16", height: "16", fill: "currentColor", className: "bi bi-info-circle", viewBox: "0 0 16 16", style: { verticalAlign: 'sub' } },
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" }),
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z" })))))),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "col-8 d-flex flex-column justify-content-center" },
                        this.props.searchable && (react__WEBPACK_IMPORTED_MODULE_0__.createElement((react_select__WEBPACK_IMPORTED_MODULE_1___default()), { options: values, value: values.find(option => option.value === selected), isDisabled: !this.props.editable, placeholder: "Select an option", onChange: this.handleSearchableChange, styles: {
                                menu: (provided) => ({
                                    ...provided,
                                    maxHeight: '300px',
                                    overflowY: 'auto',
                                    zIndex: 9999
                                })
                            } })),
                        !this.props.searchable && (react__WEBPACK_IMPORTED_MODULE_0__.createElement("select", { ref: this.selectRef, className: "data-mount-select", key: this.props.key_, disabled: !this.props.editable, name: this.props.key_, onChange: this.handleChange }, valuesReact))))),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(react_tooltip__WEBPACK_IMPORTED_MODULE_2__.Tooltip, { id: `data-mount-tooltip-${name}` })));
    }
}


/***/ }),

/***/ "./lib/components/optionrow.js":
/*!*************************************!*\
  !*** ./lib/components/optionrow.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ OptionRow)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-tooltip */ "webpack/sharing/consume/default/react-tooltip/react-tooltip");
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_tooltip__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../icon */ "./lib/icon.js");



class OptionRow extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.handleAdd = () => {
            if (this.props.addButton) {
                this.props.addButton();
            }
        };
        this.handleDel = () => {
            if (this.props.delButton) {
                this.props.delButton(this.props.index);
            }
        };
        this.state = {
            valueFirst: props.valueFirst || '',
            valueSecond: props.valueSecond || ''
        };
        this.handleKeyChange = this.handleKeyChange.bind(this);
        this.handleValueChange = this.handleValueChange.bind(this);
        this.handleDel = this.handleDel.bind(this);
        this.keyRef = react__WEBPACK_IMPORTED_MODULE_0__.createRef();
        this.valueRef = react__WEBPACK_IMPORTED_MODULE_0__.createRef();
    }
    handleKeyChange(event) {
        this.setState({ valueFirst: event.target.value });
        if (this.props.onTextChange) {
            const value = this.valueRef.current.value;
            this.props.onTextChange(this.props.index, event.target.value, value);
        }
    }
    handleValueChange(event) {
        this.setState({ valueSecond: event.target.value });
        if (this.props.onTextChange) {
            const key = this.keyRef.current.value;
            this.props.onTextChange(this.props.index, key, event.target.value);
        }
    }
    render() {
        const { valueFirst, valueSecond, placeholderFirst, placeholderSecond, editable } = this.props;
        const colElements = "col-12";
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "row" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "col-12" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "row mb-1" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: `${colElements} d-flex justify-content-center` },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { type: "text", ref: this.keyRef, value: valueFirst, onChange: this.handleKeyChange, placeholder: placeholderFirst, disabled: !editable || this.props.index == 0, className: `form-control data-mount-dialog-textfield ${this.props.invalid ? 'invalid' : ''}` }),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { type: "text", ref: this.valueRef, value: valueSecond, onChange: this.handleValueChange, placeholder: placeholderSecond, disabled: !editable, className: "form-control data-mount-dialog-textfield" }),
                        this.props.index != 0 && (react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { style: { marginLeft: "8px" }, className: "icon-button", onClick: this.handleDel, disabled: !editable },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_icon__WEBPACK_IMPORTED_MODULE_2__.DeleteIcon.react, { tag: "span", width: "16px", height: "16px" }))),
                        this.props.index == 0 && (react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { style: { marginLeft: "8px", opacity: 0, pointerEvents: "none" }, className: "icon-button", disabled: true },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_icon__WEBPACK_IMPORTED_MODULE_2__.DeleteIcon.react, { tag: "span", width: "16px", height: "16px" }))),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { style: { marginLeft: "8px" }, className: "icon-button", onClick: this.handleAdd, disabled: !editable },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_icon__WEBPACK_IMPORTED_MODULE_2__.PlusIcon.react, { tag: "span", width: "16px", height: "16px" }))))),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(react_tooltip__WEBPACK_IMPORTED_MODULE_1__.Tooltip, { id: `data-mount-tooltip-${name}` })));
    }
}


/***/ }),

/***/ "./lib/components/textfield.js":
/*!*************************************!*\
  !*** ./lib/components/textfield.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TextField: () => (/* binding */ TextField)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-tooltip */ "webpack/sharing/consume/default/react-tooltip/react-tooltip");
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_tooltip__WEBPACK_IMPORTED_MODULE_1__);


class TextField extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: props.value || '',
            showPassword: props.type === 'password' ? false : true
        };
        // Bind the methods to the instance
        this.togglePasswordVisibility = this.togglePasswordVisibility.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
        const value = event.target.value;
        this.setState({ value });
        if (this.props.onChange) {
            this.props.onChange(event);
        }
    }
    // Method to toggle password visibility
    togglePasswordVisibility() {
        this.setState(prevState => ({
            showPassword: !prevState.showPassword
        }));
    }
    // Method to get the current value of the text input
    getValue() {
        return this.state.value;
    }
    render() {
        const { label, name, value, type = 'text', placeholder, required, tooltip } = this.props;
        const { showPassword } = this.state;
        const inputType = type === 'password' && !showPassword ? 'password' : 'text';
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "row" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "col-12" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "row mb-1" },
                    label && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "col-4 col-form-label d-flex align-items-center" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", null,
                            label,
                            ":"),
                        tooltip && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { "data-tooltip-id": `data-mount-tooltip-${name}`, "data-tooltip-html": tooltip, "data-tooltip-place": "top", className: "lh-1 ms-auto data-mount-dialog-label-tooltip" },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { xmlns: "http://www.w3.org/2000/svg", width: "16", height: "16", fill: "currentColor", className: "bi bi-info-circle", viewBox: "0 0 16 16", style: { verticalAlign: 'sub' } },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" }),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z" })))))),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "col-8 d-flex flex-column justify-content-center" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "input-group" },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: inputType, value: value, name: name, onChange: this.handleChange, placeholder: placeholder, disabled: !this.props.editable, required: required, className: "form-control data-mount-dialog-textfield" }),
                            type === 'password' && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "input-group-append" },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "btn btn-light", type: "button", onClick: this.togglePasswordVisibility },
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("i", { className: `fa ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`, "aria-hidden": "true" })))))))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_tooltip__WEBPACK_IMPORTED_MODULE_1__.Tooltip, { id: `data-mount-tooltip-${name}` })));
    }
}


/***/ }),

/***/ "./lib/dialog/widget.js":
/*!******************************!*\
  !*** ./lib/dialog/widget.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MountDialogBody: () => (/* binding */ MountDialogBody),
/* harmony export */   MountDialogComponent: () => (/* binding */ MountDialogComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_dropdown__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/dropdown */ "./lib/components/dropdown.js");
/* harmony import */ var _components_textfield__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/textfield */ "./lib/components/textfield.js");
/* harmony import */ var _components_checkbox__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../components/checkbox */ "./lib/components/checkbox.js");
/* harmony import */ var _templates_b2drop__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../templates/b2drop */ "./lib/templates/b2drop.js");
/* harmony import */ var _templates_aws__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../templates/aws */ "./lib/templates/aws.js");
/* harmony import */ var _templates_s3__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../templates/s3 */ "./lib/templates/s3.js");
/* harmony import */ var _templates_webdav__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../templates/webdav */ "./lib/templates/webdav.js");
/* harmony import */ var _templates_generic__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../templates/generic */ "./lib/templates/generic.js");










class MountDialogBody extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    getValue() {
        try {
            const displayName = this.mountcomponent_ref.current.template_ref.current.getDisplayName();
            return {
                template: this.mountcomponent_ref.current.state.datamount.template,
                path: this.mountcomponent_ref.current.state.datamount.path,
                options: {
                    ...this.mountcomponent_ref.current.state.datamount.options,
                    displayName
                },
                loading: false,
                failedLoading: false
            };
        }
        catch (e) {
            return {
                template: "none",
                path: `${this.mountDir}/none`,
                options: {},
                loading: false,
                failedLoading: false
            };
        }
    }
    constructor(editable, options, templates, mountDir) {
        super();
        this.editable = editable;
        this.options = options;
        this.templates = templates;
        this.mountDir = mountDir;
        this.mountcomponent_ref = react__WEBPACK_IMPORTED_MODULE_0__.createRef();
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(MountDialogComponent, { ref: this.mountcomponent_ref, editable: this.editable, options: this.options, templates: this.templates, mountDir: this.mountDir }));
    }
}
class MountDialogComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    handleTemplateChange(key, value) {
        this.setState(prevState => {
            return {
                datamount: {
                    ...prevState.datamount,
                    template: value,
                    path: `${this.props.mountDir}/${value}`,
                }
            };
        });
    }
    handlePathChange(event) {
        const { value } = event.target;
        this.setState(prevState => ({
            datamount: {
                ...prevState.datamount,
                template: prevState.datamount.template,
                path: value,
            }
        }));
    }
    handleCheckboxChange(event) {
        const { checked } = event.target;
        this.setState(prevState => ({
            datamount: {
                ...prevState.datamount,
                template: prevState.datamount.template,
                options: {
                    ...prevState.datamount.options,
                    readonly: checked,
                }
            }
        }));
    }
    handleGenericOptionChange() {
        if (this.template_ref.current) {
            const readonly = this.state.datamount.options.readonly;
            const rowDict = this.template_ref.current.state.rows.reduce((acc, row) => {
                acc[row.valueFirst] = row.valueSecond;
                return acc;
            }, {});
            this.setState(prevState => ({
                datamount: {
                    ...prevState.datamount,
                    template: prevState.datamount.template,
                    config: {
                        ...rowDict,
                        readonly
                    }
                }
            }));
        }
    }
    constructor(props) {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
        super(props);
        this.templates_all = [
            { value: 'aws', label: 'AWS' },
            { value: 'b2drop', label: 'B2Drop' },
            {
                value: 's3',
                label: 'S3 Compliant Storage Provider'
            },
            {
                value: 'webdav',
                label: 'Webdav'
            },
            {
                value: 'generic',
                label: 'Generic'
            }
        ];
        this.handleOptionChange = (key, value) => {
            this.setState(prevState => {
                const newDatamount = {
                    ...prevState.datamount,
                    template: prevState.datamount.template,
                    config: { ...prevState.datamount.options } // Ensure config is updated immutably
                };
                if (value === null) {
                    delete newDatamount.options[key];
                }
                else {
                    newDatamount.options[key] = value;
                }
                return {
                    datamount: newDatamount
                };
            });
        };
        this.template_ref = react__WEBPACK_IMPORTED_MODULE_0__.createRef();
        this.tooltips = {
            path: `Prefix ${this.props.mountDir} will be added automatically.`,
        };
        this.state = {
            datamount: {
                template: ((_a = props.options) === null || _a === void 0 ? void 0 : _a.template) || props.templates[0],
                path: ((_b = props.options) === null || _b === void 0 ? void 0 : _b.path) || `${props.mountDir}/${props.templates[0]}`,
                options: {
                    ...(_c = props.options) === null || _c === void 0 ? void 0 : _c.options,
                    readonly: (_f = (_e = (_d = props.options) === null || _d === void 0 ? void 0 : _d.options) === null || _e === void 0 ? void 0 : _e.readonly) !== null && _f !== void 0 ? _f : false
                },
                loading: (_h = (_g = props.options) === null || _g === void 0 ? void 0 : _g.loading) !== null && _h !== void 0 ? _h : false,
                failedLoading: (_k = (_j = props.options) === null || _j === void 0 ? void 0 : _j.failedLoading) !== null && _k !== void 0 ? _k : false
            }
        };
        if (props.templates) {
            const templateOrder = new Map(props.templates.map((t, index) => [t, index]));
            this.templates = this.templates_all
                .filter(template => templateOrder.has(template.value))
                .sort((a, b) => templateOrder.get(a.value) - templateOrder.get(b.value));
        }
        else {
            this.templates = [...this.templates_all]; // Default to all templates if none are provided
        }
        this.handleTemplateChange = this.handleTemplateChange.bind(this);
        this.handlePathChange = this.handlePathChange.bind(this);
        this.handleGenericOptionChange = this.handleGenericOptionChange.bind(this);
        this.handleOptionChange = this.handleOptionChange.bind(this);
        this.handleCheckboxChange = this.handleCheckboxChange.bind(this);
    }
    render() {
        const { template } = this.state.datamount;
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_dropdown__WEBPACK_IMPORTED_MODULE_2__.DropdownComponent, { label: "Template", key_: "template", selected: this.state.datamount.template, values: this.templates, onValueChange: this.handleTemplateChange, editable: this.props.editable, searchable: true }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_3__.TextField, { label: "Mount Path", name: "path", tooltip: this.tooltips.path, value: this.state.datamount.path, editable: this.props.editable, onChange: this.handlePathChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_checkbox__WEBPACK_IMPORTED_MODULE_4__["default"], { label: "Read only", name: "readonly", checked: this.state.datamount.options.readonly, editable: this.props.editable, onChange: this.handleCheckboxChange }),
            template === 'b2drop' && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_templates_b2drop__WEBPACK_IMPORTED_MODULE_5__["default"], { onValueChange: this.handleOptionChange, ref: this.template_ref, editable: this.props.editable, options: this.state.datamount.options })),
            template === 'generic' && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_templates_generic__WEBPACK_IMPORTED_MODULE_6__["default"], { onValueChange: this.handleGenericOptionChange, ref: this.template_ref, editable: this.props.editable, options: this.state.datamount.options })),
            template === 'aws' && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_templates_aws__WEBPACK_IMPORTED_MODULE_7__["default"], { onValueChange: this.handleOptionChange, ref: this.template_ref, editable: this.props.editable, options: this.state.datamount.options })),
            template === 's3' && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_templates_s3__WEBPACK_IMPORTED_MODULE_8__["default"], { onValueChange: this.handleOptionChange, ref: this.template_ref, editable: this.props.editable, options: this.state.datamount.options })),
            template === 'webdav' && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_templates_webdav__WEBPACK_IMPORTED_MODULE_9__["default"], { onValueChange: this.handleOptionChange, ref: this.template_ref, editable: this.props.editable, options: this.state.datamount.options }))));
    }
}


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   RequestAddMountPoint: () => (/* binding */ RequestAddMountPoint),
/* harmony export */   RequestGetMountDir: () => (/* binding */ RequestGetMountDir),
/* harmony export */   RequestGetTemplates: () => (/* binding */ RequestGetTemplates),
/* harmony export */   RequestRemoveMountPoint: () => (/* binding */ RequestRemoveMountPoint),
/* harmony export */   listAllMountpoints: () => (/* binding */ listAllMountpoints),
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param path Path argument, must be encoded
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(path = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'data-mount', // API Namespace
    path);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}
async function listAllMountpoints() {
    let mountPoints = [];
    try {
        const data = await requestAPI("");
        mountPoints = data;
    }
    catch (reason) {
        console.error(`Data Mount: Could not receive MountPoints.\n${reason}`);
        throw new Error(`Failed to fetch mount points\n${reason}`);
    }
    return mountPoints;
}
async function RequestAddMountPoint(mountPoint) {
    try {
        await requestAPI('', {
            body: JSON.stringify(mountPoint),
            method: "POST"
        });
    }
    catch (reason) {
        console.error(`Data Mount: Could not add MountPoint.\n${reason}`);
        throw new Error(`Failed to add mount point.\n${reason}`);
    }
}
async function RequestGetTemplates() {
    let data = [];
    try {
        data = await requestAPI('templates', {
            method: "GET"
        });
    }
    catch (reason) {
        data = ["aws", "b2drop", "s3", "webdav", "generic"];
        console.error(`Data Mount: Could not get templates.\n${reason}`);
        throw new Error(`Failed to get templates.\n${reason}`);
    }
    return data;
}
async function RequestGetMountDir() {
    let data = [];
    try {
        data = await requestAPI('mountdir', {
            method: "GET"
        });
    }
    catch (reason) {
        data = ["aws", "b2drop", "s3", "webdav", "generic"];
        console.error(`Data Mount: Could not get templates.\n${reason}`);
        throw new Error(`Failed to get templates.\n${reason}`);
    }
    return data;
}
async function RequestRemoveMountPoint(mountPoint) {
    const pathEncoded = encodeURIComponent(mountPoint.path);
    try {
        await requestAPI(pathEncoded, {
            body: JSON.stringify(mountPoint),
            method: "DELETE",
        });
    }
    catch (reason) {
        if (reason) {
            throw new Error(`${reason}`);
        }
        else {
            throw new Error('Failed to delete mount point.');
        }
    }
}


/***/ }),

/***/ "./lib/icon.js":
/*!*********************!*\
  !*** ./lib/icon.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DeleteIcon: () => (/* binding */ DeleteIcon),
/* harmony export */   DirectoryIcon: () => (/* binding */ DirectoryIcon),
/* harmony export */   PlusIcon: () => (/* binding */ PlusIcon),
/* harmony export */   RefreshIcon: () => (/* binding */ RefreshIcon),
/* harmony export */   SettingsIcon: () => (/* binding */ SettingsIcon),
/* harmony export */   StopIcon: () => (/* binding */ StopIcon),
/* harmony export */   cloudStorageIcon: () => (/* binding */ cloudStorageIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_img_cloud_storage_icon_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/img/cloud-storage-icon.svg */ "./style/img/cloud-storage-icon.svg");
/* harmony import */ var _style_img_plus_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/img/plus.svg */ "./style/img/plus.svg");
/* harmony import */ var _style_img_delete_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/img/delete.svg */ "./style/img/delete.svg");
/* harmony import */ var _style_img_refresh_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/img/refresh.svg */ "./style/img/refresh.svg");
/* harmony import */ var _style_img_directory_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/img/directory.svg */ "./style/img/directory.svg");
/* harmony import */ var _style_img_settings_svg__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/img/settings.svg */ "./style/img/settings.svg");
/* harmony import */ var _style_img_stop_svg__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/img/stop.svg */ "./style/img/stop.svg");








const cloudStorageIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jupyterlab-data-mount:cloud-storage',
    svgstr: _style_img_cloud_storage_icon_svg__WEBPACK_IMPORTED_MODULE_1__
});
const PlusIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jupyterlab-data-mount:plus-icon',
    svgstr: _style_img_plus_svg__WEBPACK_IMPORTED_MODULE_2__
});
const DeleteIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jupyterlab-data-mount:delete-icon',
    svgstr: _style_img_delete_svg__WEBPACK_IMPORTED_MODULE_3__
});
const RefreshIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jupyterlab-data-mount:refresh-icon',
    svgstr: _style_img_refresh_svg__WEBPACK_IMPORTED_MODULE_4__
});
const DirectoryIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jupyterlab-data-mount:dir-icon',
    svgstr: _style_img_directory_svg__WEBPACK_IMPORTED_MODULE_5__
});
const SettingsIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jupyterlab-data-mount:settings-icon',
    svgstr: _style_img_settings_svg__WEBPACK_IMPORTED_MODULE_6__
});
const StopIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jupyterlab-data-mount:stop-icon',
    svgstr: _style_img_stop_svg__WEBPACK_IMPORTED_MODULE_7__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _sidebar_widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./sidebar/widget */ "./lib/sidebar/widget.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var bootstrap_dist_css_bootstrap_min_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");





/**
 * Initialization data for the jupyterlab-data-mount extension.
 */
const plugin = {
    id: 'jupyterlab-data-mount:plugin',
    description: 'A JupyterLab extension to mount external data storage locations.',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: activate
};
async function activate(app, palette) {
    console.log('JupyterLab extension jupyterlab-data-mount is activated!');
    const templates = await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.RequestGetTemplates)();
    const mountDir = await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.RequestGetMountDir)();
    let sbwidget = new _sidebar_widget__WEBPACK_IMPORTED_MODULE_3__.SideBarWidget(app, app.commands, _commands__WEBPACK_IMPORTED_MODULE_4__.CommandIDs.opendialog, templates, mountDir);
    app.shell.add(sbwidget, 'left');
    app.shell.activateById(sbwidget.id);
    (0,_commands__WEBPACK_IMPORTED_MODULE_4__.addCommands)(app, sbwidget, templates, mountDir);
    palette.addItem({
        command: _commands__WEBPACK_IMPORTED_MODULE_4__.CommandIDs.opendialog,
        category: 'Data'
    });
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/sidebar/body.js":
/*!*****************************!*\
  !*** ./lib/sidebar/body.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ SideBarBody)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../icon */ "./lib/icon.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _dialog_widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../dialog/widget */ "./lib/dialog/widget.js");




class SideBarBody extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "data-mount-sidebar" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "data-mount-sidebar-header" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "header-item name" }, "Mount"),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "header-item actions" }, "Actions")),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("ul", { className: "data-mount-sidebar-list" }, this.props.mountPoints.map(mount => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(MountRowElement, { mount: mount, commands: this.props.commands, templates: this.props.templates, mountDir: this.props.mountDir, removeMountPoint: this.props.removeMountPoint }))))));
    }
}
class MountRowElement extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.openDirectory = () => {
            this.props.commands.execute('filebrowser:open-path', { path: `${this.props.mount.path}` });
        };
        this.openDialog = () => {
            const buttons = [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Ok' })];
            const options = {
                template: this.props.mount.template,
                path: this.props.mount.path,
                options: { ...this.props.mount.options }
            };
            const body = new _dialog_widget__WEBPACK_IMPORTED_MODULE_2__.MountDialogBody(false, options, this.props.templates, this.props.mountDir);
            body.node.style.overflow = 'visible';
            body.node.className = 'data-mount-dialog-body';
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: 'Data Mount',
                body: body,
                buttons: buttons
            });
        };
    }
    render() {
        const loading = this.props.mount.loading || false;
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", { key: this.props.mount.options.displayName, className: "data-mount-sidebar-item" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: `item-name ${this.props.mount.options.external || loading ? "external" : ""}` },
                this.props.mount.options.displayName,
                loading ? " ( loading ... )" : ""),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: "item-actions" },
                !loading && (react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "icon-button", title: `Open ${this.props.mountDir}/${this.props.mount.path}`, onClick: () => this.openDirectory() },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_icon__WEBPACK_IMPORTED_MODULE_3__.DirectoryIcon.react, { tag: "span", width: "16px", height: "16px" }))),
                !loading && !this.props.mount.options.external && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "icon-button", title: "Show options", onClick: this.openDialog },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_icon__WEBPACK_IMPORTED_MODULE_3__.SettingsIcon.react, { tag: "span", width: "16px", height: "16px" })),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "icon-button unmount", title: "Unmount", onClick: async () => {
                            try {
                                await this.props.removeMountPoint(this.props.mount);
                            }
                            catch (error) {
                                console.error("Unmount failed:", error);
                            }
                        } },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_icon__WEBPACK_IMPORTED_MODULE_3__.StopIcon.react, { tag: "span", width: "16px", height: "16px" })))))));
    }
}


/***/ }),

/***/ "./lib/sidebar/header.js":
/*!*******************************!*\
  !*** ./lib/sidebar/header.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ SideBarHeader)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Button__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/Button */ "./node_modules/@mui/material/Button/Button.js");
/* harmony import */ var _mui_icons_material_Add__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/icons-material/Add */ "./node_modules/@mui/icons-material/esm/Add.js");
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-tooltip */ "webpack/sharing/consume/default/react-tooltip/react-tooltip");
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_tooltip__WEBPACK_IMPORTED_MODULE_1__);




class SideBarHeader extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    render() {
        const onClick = () => this.props.commands.execute(this.props.commandId);
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "data-mount-sidepanel-header container mb-3" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { "data-tooltip-id": `data-mount-tooltip-documentation`, "data-tooltip-html": "Click for documentation", "data-tooltip-place": "left", className: "data-mount-sidepanel-header-documentation lh-1 ms-auto data-mount-dialog-label-tooltip", href: "https://www.google.com", target: "_blank" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", { xmlns: "http://www.w3.org/2000/svg", width: "16", height: "16", fill: "currentColor", className: "bi bi-info-circle", viewBox: "0 0 16 16", style: { verticalAlign: 'sub' } },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" }),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z" }))),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "data-mount-sidepanel-header-button-div mt-3" },
                    this.props.failedLoading && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "contained", size: "small", disabled: true }, "Start failed."),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, "Check logs in Browser for more information"))),
                    !this.props.failedLoading && this.props.loading && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "contained", size: "small", disabled: true }, "Loading ...")),
                    !this.props.failedLoading && !this.props.loading && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "contained", size: "small", startIcon: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_icons_material_Add__WEBPACK_IMPORTED_MODULE_3__["default"], null), onClick: onClick }, "Add Mount"))),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("hr", null)),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(react_tooltip__WEBPACK_IMPORTED_MODULE_1__.Tooltip, { id: `data-mount-tooltip-documentation` })));
    }
}


/***/ }),

/***/ "./lib/sidebar/widget.js":
/*!*******************************!*\
  !*** ./lib/sidebar/widget.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SideBarWidget: () => (/* binding */ SideBarWidget),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../icon */ "./lib/icon.js");
/* harmony import */ var _header__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./header */ "./lib/sidebar/header.js");
/* harmony import */ var _body__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./body */ "./lib/sidebar/body.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");






class SideBarComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this._app = props.app;
        this._commands = props.commands;
        this._openCommandId = props.commandId;
        this._templates = props.templates;
        this._mountDir = props.mountDir;
        this.removeMountPoint = this.removeMountPoint.bind(this);
        this.state = {
            mountPoints: [],
            globalLoading: true,
            globalLoadingFailed: false
        };
    }
    async reloadMountPoints() {
        try {
            const mountPoints = await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.listAllMountpoints)();
            this.setState({
                mountPoints,
                globalLoading: false
            });
        }
        catch (_a) {
            this.setState({ globalLoadingFailed: true, globalLoading: false });
        }
    }
    async componentDidMount() {
        await this.reloadMountPoints();
    }
    setMountPointLoaded(mountPoint) {
        this.setState(prevState => ({
            mountPoints: prevState.mountPoints.map(mp => mp.path === mountPoint.path
                ? { ...mp, loading: false }
                : mp)
        }));
    }
    addMountPoint(mountPoint) {
        this.setState(prevState => ({
            mountPoints: [...prevState.mountPoints, mountPoint]
        }));
    }
    addFailedMountPoint(mountPoint) {
        this.setState(prevState => ({
            mountPoints: [...prevState.mountPoints, mountPoint]
        }));
    }
    async removeMountPoint(mountPoint, force) {
        try {
            await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.RequestRemoveMountPoint)(mountPoint);
            this.setState(prevState => ({
                mountPoints: prevState.mountPoints.filter(mountPoint_ => mountPoint_.path !== mountPoint.path)
            }));
        }
        catch (reason) {
            if (force) {
                try {
                    this.setState(prevState => ({
                        mountPoints: prevState.mountPoints.filter(mountPoint_ => mountPoint_.path !== mountPoint.path)
                    }));
                }
                catch (_a) { }
            }
            else {
                alert(`Could not unmount ${mountPoint.options.displayName}.\nCheck ${this.props.mountDir}/mount.log for details`);
            }
        }
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("body", null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_header__WEBPACK_IMPORTED_MODULE_3__["default"], { commands: this._commands, commandId: this._openCommandId, loading: this.state.globalLoading, failedLoading: this.state.globalLoadingFailed }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_body__WEBPACK_IMPORTED_MODULE_4__["default"], { app: this._app, commands: this._commands, commandId: this._openCommandId, templates: this._templates, mountDir: this._mountDir, loading: this.state.globalLoading, mountPoints: this.state.mountPoints, removeMountPoint: this.removeMountPoint })));
    }
}
class SideBarWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(app, commands, openCommandId, templates, mountDir) {
        super();
        this._sidebarComponentRef = react__WEBPACK_IMPORTED_MODULE_0__.createRef();
        this._app = app;
        this.id = 'data-mount-jupyterlab:sidebarwidget';
        this.title.caption = 'Data Mount';
        this._commands = commands;
        this._openCommandId = openCommandId;
        this._templates = templates;
        this._mountDir = mountDir;
        this.title.icon = _icon__WEBPACK_IMPORTED_MODULE_5__.cloudStorageIcon;
        this.addClass('jp-data-mount');
    }
    async removeMountPoint(mountPoint, force) {
        if (this._sidebarComponentRef.current) {
            await this._sidebarComponentRef.current.removeMountPoint(mountPoint, force);
        }
    }
    addMountPoint(mountPoint) {
        if (this._sidebarComponentRef.current) {
            this._sidebarComponentRef.current.addMountPoint(mountPoint);
        }
    }
    setMountPointLoaded(mountPoint) {
        if (this._sidebarComponentRef.current) {
            this._sidebarComponentRef.current.setMountPointLoaded(mountPoint);
        }
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("body", null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(SideBarComponent, { ref: this._sidebarComponentRef, app: this._app, commands: this._commands, commandId: this._openCommandId, templates: this._templates, mountDir: this._mountDir })));
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SideBarWidget);


/***/ }),

/***/ "./lib/templates/aws.js":
/*!******************************!*\
  !*** ./lib/templates/aws.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ AWS)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_dropdown__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/dropdown */ "./lib/components/dropdown.js");
/* harmony import */ var _components_textfield__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/textfield */ "./lib/components/textfield.js");
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base */ "./lib/templates/base.js");




class AWS extends _base__WEBPACK_IMPORTED_MODULE_1__.BaseComponent {
    constructor(props) {
        super(props);
        this.tooltips = {
            remotepath: 'The name of the bucket to mount',
            access_key_id: 'AWS Access Key ID',
            secret_access_key: 'AWS Secret Access Key (password)',
            region: 'Region to connect to'
        };
        this.awsRegions = [
            { value: 'eu-north-1', label: 'EU (Stockholm) (eu-north-1)' },
            { value: 'eu-central-1', label: 'EU (Frankfurt) (eu-central-1)' },
            { value: 'eu-west-1', label: 'EU (Ireland) (eu-west-1)' },
            { value: 'eu-west-2', label: 'EU (London) (eu-west-2)' },
            { value: 'ca-central-1', label: 'Canada (Central) (ca-central-1)' },
            { value: 'us-east-1', label: 'US East (Northern Virginia) (us-east-1)' },
            { value: 'us-east-2', label: 'US East (Ohio) (us-east-2)' },
            { value: 'us-west-1', label: 'US West (Northern California) (us-west-1)' },
            { value: 'us-west-2', label: 'US West (Oregon) (us-west-2)' },
            {
                value: 'ap-southeast-1',
                label: 'Asia Pacific (Singapore) (ap-southeast-1)'
            },
            {
                value: 'ap-southeast-2',
                label: 'Asia Pacific (Sydney) (ap-southeast-2)'
            },
            { value: 'ap-northeast-1', label: 'Asia Pacific (Tokyo) (ap-northeast-1)' },
            { value: 'ap-northeast-2', label: 'Asia Pacific (Seoul) (ap-northeast-2)' },
            { value: 'ap-south-1', label: 'Asia Pacific (Mumbai) (ap-south-1)' },
            { value: 'sa-east-1', label: 'South America (Sao Paulo) (sa-east-1)' }
        ];
        if (!props.editable && props.options && Object.keys(props.options).length > 0) {
            this.state = props.options;
        }
        else {
            this.state = {
                remotepath: 'bucketname',
                type: 's3',
                provider: 'AWS',
                access_key_id: '',
                secret_access_key: '',
                region: 'eu-north-1'
            };
        }
    }
    getDisplayName() {
        return `AWS (${this.state.remotepath})`;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "data-mount-dialog-options" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "row mb-1 data-mount-dialog-config-header" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, "AWS Configuration")),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_2__.TextField, { label: "Bucket Name", name: "remotepath", value: this.state.remotepath, onChange: this.handleTextFieldChange, editable: this.props.editable }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_dropdown__WEBPACK_IMPORTED_MODULE_3__.DropdownComponent, { label: "Region", key_: "region", selected: this.state.region, values: this.awsRegions, tooltip: this.tooltips.region, onValueChange: this.handleDropdownChange, editable: this.props.editable, searchable: true }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_2__.TextField, { label: "Username", name: "access_key_id", tooltip: this.tooltips.access_key_id, value: this.state.access_key_id, editable: this.props.editable, onChange: this.handleTextFieldChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_2__.TextField, { label: "Password", name: "secret_access_key", type: "password", tooltip: this.tooltips.secret_access_key, value: this.state.secret_access_key, editable: this.props.editable, onChange: this.handleTextFieldChange })));
    }
}


/***/ }),

/***/ "./lib/templates/b2drop.js":
/*!*********************************!*\
  !*** ./lib/templates/b2drop.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ B2Drop)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_textfield__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/textfield */ "./lib/components/textfield.js");
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base */ "./lib/templates/base.js");



class B2Drop extends _base__WEBPACK_IMPORTED_MODULE_1__.BaseComponent {
    constructor(props) {
        super(props);
        this.tooltips = {
            remotepath: '',
            user: 'User name or App name',
            obscure_pass: 'Password or App password'
        };
        this.handleUserTextFieldChange = this.handleUserTextFieldChange.bind(this);
        if (!props.editable && props.options && Object.keys(props.options).length > 0) {
            this.state = props.options;
        }
        else {
            this.state = {
                remotepath: '/',
                type: 'webdav',
                url: 'https://b2drop.eudat.eu/remote.php/webdav/',
                vendor: 'nextcloud',
                user: '',
                obscure_pass: ''
            };
        }
    }
    getDisplayName() {
        return 'B2Drop';
    }
    handleUserTextFieldChange(event) {
        const value = event.target.value;
        this.setState({
            user: value,
            url: `https://b2drop.eudat.eu/dav/files/${value}/`,
        }, () => {
            if (this.props.onValueChange) {
                this.props.onValueChange("user", value);
                this.props.onValueChange("url", `https://b2drop.eudat.eu/dav/files/${value}/`);
            }
        });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "data-mount-dialog-options" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "row mb-1 data-mount-dialog-config-header" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, "B2Drop Configuration")),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_2__.TextField, { label: "User", name: "user", tooltip: this.tooltips.user, value: this.state.user, editable: this.props.editable, onChange: this.handleUserTextFieldChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_2__.TextField, { label: "Password", type: "password", name: "obscure_pass", tooltip: this.tooltips.obscure_pass, value: this.state.obscure_pass, editable: this.props.editable, onChange: this.handleTextFieldChange })));
    }
}


/***/ }),

/***/ "./lib/templates/base.js":
/*!*******************************!*\
  !*** ./lib/templates/base.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BaseComponent: () => (/* binding */ BaseComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

class BaseComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.handleDropdownChange = this.handleDropdownChange.bind(this);
        this.handleTextFieldChange = this.handleTextFieldChange.bind(this);
    }
    componentWillUnmount() {
        Object.keys(this.state).forEach(key => {
            this.props.onValueChange(key, null);
        });
    }
    componentDidMount() {
        Object.entries(this.state).forEach(([key, value]) => {
            this.props.onValueChange(key, value);
        });
    }
    getDisplayName() {
        return `Replace in subclass`;
    }
    handleDropdownChange(key, value) {
        this.setState({ [key]: value }, () => {
            if (this.props.onValueChange) {
                this.props.onValueChange(key, value);
            }
        });
    }
    handleTextFieldChange(event) {
        const { name, value } = event.target;
        this.setState({ [name]: value }, () => {
            if (this.props.onValueChange) {
                this.props.onValueChange(name, value);
            }
        });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("h2", null, "Replace in specific mount type")));
    }
}


/***/ }),

/***/ "./lib/templates/generic.js":
/*!**********************************!*\
  !*** ./lib/templates/generic.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ Generic)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_optionrow__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/optionrow */ "./lib/components/optionrow.js");
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./base */ "./lib/templates/base.js");
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-tooltip */ "webpack/sharing/consume/default/react-tooltip/react-tooltip");
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_tooltip__WEBPACK_IMPORTED_MODULE_1__);




class Generic extends _base__WEBPACK_IMPORTED_MODULE_2__.BaseComponent {
    constructor(props) {
        super(props);
        if (!props.editable && props.options && Object.keys(props.options).length > 0) {
            const rows = Object.entries(props.options).filter(([key, value]) => !["displayName", "readonly"].includes(key)).map(([key, value], index) => ({
                valueFirst: key,
                valueSecond: value,
                invalid: false,
                index: index
            }));
            this.state = {
                rows: rows
            };
        }
        else {
            this.state = {
                rows: [{
                        valueFirst: 'type',
                        valueSecond: 's3',
                        invalid: false,
                        index: 0
                    }]
            };
        }
        this.onTextChange = this.onTextChange.bind(this);
        this.addRow = this.addRow.bind(this);
        this.delRow = this.delRow.bind(this);
    }
    onTextChange(index, key, value) {
        // check for duplicated keys
        const isKeyDuplicate = this.state.rows.some((row) => row.index !== index && row.valueFirst === key && !row.invalid);
        // Update row with row.index == index
        const updatedRows = this.state.rows.map((row) => {
            if (row.index === index) {
                return {
                    ...row,
                    valueFirst: key,
                    valueSecond: value,
                    invalid: isKeyDuplicate
                };
            }
            return row;
        });
        this.setState({ rows: updatedRows }, () => {
            if (this.props.onValueChange) {
                this.props.onValueChange();
            }
        });
    }
    getValue() {
        const rowDict = this.state.rows.reduce((acc, row) => {
            acc[row.valueFirst] = row.valueSecond;
            return acc;
        }, {});
        return rowDict;
    }
    addRow() {
        const newIndex = this.state.rows[this.state.rows.length - 1].index + 1;
        const newRow = {
            valueFirst: '',
            valueSecond: '',
            invalid: false,
            index: newIndex
        };
        this.setState(prevState => ({
            rows: [...prevState.rows, newRow]
        }));
    }
    delRow(index) {
        const updatedRows = this.state.rows.filter((row) => row.index !== index);
        this.setState({ rows: updatedRows }, () => {
            if (this.props.onValueChange) {
                this.props.onValueChange();
            }
        });
    }
    getDisplayName() {
        return `Generic ${this.state.rows[0].valueSecond}`;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "data-mount-dialog-options" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "row mb-1 data-mount-dialog-config-header" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null,
                        "Generic Configuration",
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { "data-tooltip-id": `data-mount-generic-tooltip`, "data-tooltip-html": "Click for documentation", "data-tooltip-place": "left", className: "data-mount-generic-tooltip lh-1 ms-1 data-mount-dialog-label-tooltip", href: "https://www.google.com", target: "_blank" },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", { xmlns: "http://www.w3.org/2000/svg", width: "16", height: "16", fill: "currentColor", className: "bi bi-info-circle", viewBox: "0 0 16 16", style: { verticalAlign: 'sub' } },
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" }),
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z" }))))),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(react_tooltip__WEBPACK_IMPORTED_MODULE_1__.Tooltip, { id: `data-mount-generic-tooltip` }),
                this.state.rows.map(row => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_optionrow__WEBPACK_IMPORTED_MODULE_3__["default"], { index: row.index, totalCount: this.state.rows.length, valueFirst: row.valueFirst, valueSecond: row.valueSecond, invalid: row.invalid, onTextChange: this.onTextChange, addButton: this.addRow, delButton: this.delRow, placeholderFirst: "key", placeholderSecond: "value", editable: this.props.editable }))))));
    }
}


/***/ }),

/***/ "./lib/templates/s3.js":
/*!*****************************!*\
  !*** ./lib/templates/s3.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ S3)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_dropdown__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/dropdown */ "./lib/components/dropdown.js");
/* harmony import */ var _components_textfield__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/textfield */ "./lib/components/textfield.js");
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base */ "./lib/templates/base.js");




class S3 extends _base__WEBPACK_IMPORTED_MODULE_1__.BaseComponent {
    constructor(props) {
        super(props);
        this.providerOptions = [
            {
                value: 'AWS',
                label: 'Amazon Web Services (AWS) S3'
            },
            {
                value: 'Alibaba',
                label: 'Alibaba Cloud Object Storage System (OSS) formerly Aliyun'
            },
            {
                value: 'Ceph',
                label: 'Ceph Object Storage'
            },
            {
                value: 'DigitalOcean',
                label: 'Digital Ocean Spaces'
            },
            {
                value: 'Dreamhost',
                label: 'Dreamhost DreamObjects'
            },
            {
                value: 'IBMCOS',
                label: 'IBM COS S3'
            },
            {
                value: 'Minio',
                label: 'Minio Object Storage'
            },
            {
                value: 'Netease',
                label: 'Netease Object Storage (NOS)'
            },
            {
                value: 'Wasabi',
                label: 'Wasabi Object Storage'
            },
            {
                value: 'Other',
                label: 'Any other S3 compatible provider'
            }
        ];
        this.tooltips = {
            remotepath: 'The name of the bucket to mount',
            provider: 'Choose your S3 provider.',
            access_key_id: 'AWS Access Key ID',
            secret_access_key: 'AWS Secret Access Key (password)',
            endpoint: 'Endpoint for S3 API.<br />\
       Required when using an S3 clone',
            region: "Leave blank if you are using an S3 clone and you don't have a region"
        };
        if (!props.editable && props.options && Object.keys(props.options).length > 0) {
            this.state = props.options;
        }
        else {
            this.state = {
                remotepath: 'bucketname',
                type: 's3',
                provider: '',
                access_key_id: '',
                secret_access_key: '',
                endpoint: '',
                region: ''
            };
        }
    }
    getDisplayName() {
        return `S3 (${this.state.provider})`;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "data-mount-dialog-options" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "row mb-1 data-mount-dialog-config-header" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, "S3 Compliant Storage Provider Configuration")),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_dropdown__WEBPACK_IMPORTED_MODULE_2__.DropdownComponent, { label: "Provider", key_: "provider", tooltip: this.tooltips.provider, selected: this.state.provider, values: this.providerOptions, onValueChange: this.handleDropdownChange, editable: this.props.editable, searchable: true }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_3__.TextField, { label: "Bucket Name", name: "remotepath", value: this.state.remotepath, editable: this.props.editable, onChange: this.handleTextFieldChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_3__.TextField, { label: "Endpoint for S3 API", name: "endpoint", tooltip: this.tooltips.endpoint, value: this.state.endpoint, editable: this.props.editable, onChange: this.handleTextFieldChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_3__.TextField, { label: "Username", name: "access_key_id", tooltip: this.tooltips.access_key_id, value: this.state.access_key_id, editable: this.props.editable, onChange: this.handleTextFieldChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_3__.TextField, { label: "Password", name: "secret_access_key", type: "password", tooltip: this.tooltips.secret_access_key, value: this.state.secret_access_key, editable: this.props.editable, onChange: this.handleTextFieldChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_3__.TextField, { label: "Region", name: "region", tooltip: this.tooltips.region, value: this.state.region, editable: this.props.editable, onChange: this.handleTextFieldChange })));
    }
}


/***/ }),

/***/ "./lib/templates/webdav.js":
/*!*********************************!*\
  !*** ./lib/templates/webdav.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ Webdav)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_dropdown__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/dropdown */ "./lib/components/dropdown.js");
/* harmony import */ var _components_textfield__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/textfield */ "./lib/components/textfield.js");
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base */ "./lib/templates/base.js");




class Webdav extends _base__WEBPACK_IMPORTED_MODULE_1__.BaseComponent {
    constructor(props) {
        super(props);
        this.tooltips = {
            remotepath: '',
            type: '',
            url: 'URL of http host to connect to',
            vendor: 'Name of the Webdav site/service/software you are using',
            user: 'User name or App name',
            obscure_pass: 'Password or App password',
            bearer_token: 'Bearer token instead of user/pass (eg a Macaroon)'
        };
        this.vendorOptions = [
            {
                value: 'nextcloud',
                label: 'Nextcloud'
            },
            {
                value: 'owncloud',
                label: 'Owncloud'
            },
            {
                value: 'sharepoint',
                label: 'Sharepoint'
            },
            {
                value: 'other',
                label: 'Other site/service or software'
            }
        ];
        if (!props.editable && props.options && Object.keys(props.options).length > 0) {
            this.state = props.options;
        }
        else {
            this.state = {
                remotepath: '/',
                type: 'webdav',
                url: 'https://b2drop.eudat.eu/remote.php/webdav/',
                vendor: 'nextcloud',
                user: '',
                obscure_pass: '',
                bearer_token: ''
            };
        }
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "data-mount-dialog-options" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "row mb-1 data-mount-dialog-config-header" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, "B2Drop Configuration")),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_2__.TextField, { label: "URL", name: "url", tooltip: this.tooltips.url, value: this.state.url, editable: this.props.editable, onChange: this.handleTextFieldChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_dropdown__WEBPACK_IMPORTED_MODULE_3__.DropdownComponent, { label: "Vendor", key_: "vendor", tooltip: this.tooltips.vendor, selected: this.state.vendor, values: this.vendorOptions, onValueChange: this.handleDropdownChange, editable: this.props.editable, searchable: true }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_2__.TextField, { label: "User", name: "user", tooltip: this.tooltips.user, value: this.state.user, editable: this.props.editable, onChange: this.handleTextFieldChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_2__.TextField, { label: "Password", type: "password", name: "obscure_pass", tooltip: this.tooltips.obscure_pass, value: this.state.obscure_pass, editable: this.props.editable, onChange: this.handleTextFieldChange }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_textfield__WEBPACK_IMPORTED_MODULE_2__.TextField, { label: "Bearer Token (optional)", name: "bearer_token", tooltip: this.tooltips.bearer_token, value: this.state.bearer_token, editable: this.props.editable, onChange: this.handleTextFieldChange })));
    }
}


/***/ }),

/***/ "./style/img/cloud-storage-icon.svg":
/*!******************************************!*\
  !*** ./style/img/cloud-storage-icon.svg ***!
  \******************************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   viewBox=\"0 0 122.87 108.46\"\n   width=\"20\"\n   height=\"20\"\n   version=\"1.1\"\n   id=\"svg999\"\n   sodipodi:docname=\"cloud-storage-icon.svg\"\n   inkscape:version=\"1.1.2 (b8e25be833, 2022-02-05)\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\"\n   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n   xmlns:cc=\"http://creativecommons.org/ns#\"\n   xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\n  <sodipodi:namedview\n     id=\"namedview1001\"\n     pagecolor=\"#ffffff\"\n     bordercolor=\"#666666\"\n     borderopacity=\"1.0\"\n     inkscape:pageshadow=\"2\"\n     inkscape:pageopacity=\"0.0\"\n     inkscape:pagecheckerboard=\"0\"\n     showgrid=\"false\"\n     inkscape:zoom=\"20.125\"\n     inkscape:cx=\"3.2049689\"\n     inkscape:cy=\"2.9068323\"\n     inkscape:window-width=\"1920\"\n     inkscape:window-height=\"1001\"\n     inkscape:window-x=\"-9\"\n     inkscape:window-y=\"-9\"\n     inkscape:window-maximized=\"1\"\n     inkscape:current-layer=\"svg999\" />\n  <defs\n     id=\"defs993\">\n    <style\n       id=\"style991\">.cls-1{fill-rule:evenodd;}</style>\n  </defs>\n  <title\n     id=\"title995\">cloud-storage</title>\n  <path\n     class=\"cls-1\"\n     d=\"M23.88,0H69C77.1,0,83.12,5.72,85.31,13.25c.66.26,1.33.54,2,.86A27.39,27.39,0,0,1,100,26.62h0a21.22,21.22,0,0,1,3.55-.27,18.22,18.22,0,0,1,13.57,5.9,21.67,21.67,0,0,1,2.24,2.89,24.42,24.42,0,0,1,3.54,13.29A21.84,21.84,0,0,1,119,61.2a20.24,20.24,0,0,1-6.43,5.5,32.53,32.53,0,0,1-8.66,3.21l-.61.08H92l.22,2c.4,3.51.85,7,1.19,10.53.24,2.39.41,4.6.48,6.65a36.36,36.36,0,0,1-.56,8.82.58.58,0,0,1,0,.14A11.38,11.38,0,0,1,82,108.46H11.6A11.32,11.32,0,0,1,3.45,105C.12,101.53.29,98.39.16,94.27.09,92.22,0,90,0,87.79A109.64,109.64,0,0,1,.9,74.31L6.85,17c.94-9,7.44-17,17-17ZM89.12,37.94l-3.59-4.11a30.24,30.24,0,0,1,4-3.12,28,28,0,0,1,3.55-2c.49-.25,1-.48,1.49-.69a21.9,21.9,0,0,0-9.63-9,23.45,23.45,0,0,0-12.38-2.15A22.38,22.38,0,0,0,61,21.38a21.78,21.78,0,0,0-8,13.45l-.35,1.87L50.82,37A24.75,24.75,0,0,0,46,38.34a15.89,15.89,0,0,0-3.68,2A11.76,11.76,0,0,0,40,42.39a12.6,12.6,0,0,0-2.83,8.23A14.87,14.87,0,0,0,40,59.17a13.62,13.62,0,0,0,2.34,2.52,11.7,11.7,0,0,0,3.07,1.84,15.64,15.64,0,0,0,3.77,1H103A27.46,27.46,0,0,0,109.88,62a14.78,14.78,0,0,0,4.74-4,16.35,16.35,0,0,0,2.81-9.54,18.9,18.9,0,0,0-2.67-10.28A15.17,15.17,0,0,0,113.09,36a12.85,12.85,0,0,0-9.6-4.16c-5.74-.06-10.1,2.66-14.37,6.14ZM80.3,85.79h9.14c-.16-2.54-.44-5.45-.79-8.42a6.68,6.68,0,0,0-2.46-.46H8.48a6.81,6.81,0,0,0-3,.71c-.33,2.35-.73,5.27-.92,8.17H80.3ZM13.22,93.31H31.9v8.08H13.22V93.31Z\"\n     id=\"path997\" />\n  <metadata\n     id=\"metadata30870\">\n    <rdf:RDF>\n      <cc:Work\n         rdf:about=\"\">\n        <dc:title>cloud-storage</dc:title>\n      </cc:Work>\n    </rdf:RDF>\n  </metadata>\n</svg>\n";

/***/ }),

/***/ "./style/img/delete.svg":
/*!******************************!*\
  !*** ./style/img/delete.svg ***!
  \******************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"currentColor\" class=\"bi bi-trash-fill\" viewBox=\"0 0 16 16\">\n  <path d=\"M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z\"/>\n</svg>";

/***/ }),

/***/ "./style/img/directory.svg":
/*!*********************************!*\
  !*** ./style/img/directory.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" viewBox=\"0 0 24 24\" data-icon=\"ui-components:folder\" data-icon-id=\"b3d8f824-5e88-4660-a390-70f5f1886e4d\"><path fill=\"#616161\" d=\"M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8z\" class=\"jp-icon3 jp-icon-selectable\"></path></svg>";

/***/ }),

/***/ "./style/img/plus.svg":
/*!****************************!*\
  !*** ./style/img/plus.svg ***!
  \****************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" fill=\"currentColor\" class=\"bi bi-plus-lg m-auto\" viewBox=\"0 0 16 16\">\n  <path fill-rule=\"evenodd\" d=\"M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z\"></path>\n</svg>";

/***/ }),

/***/ "./style/img/refresh.svg":
/*!*******************************!*\
  !*** ./style/img/refresh.svg ***!
  \*******************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"currentColor\" class=\"bi bi-arrow-clockwise\" viewBox=\"0 0 16 16\">\n  <path fill-rule=\"evenodd\" d=\"M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z\"/>\n  <path d=\"M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z\"/>\n</svg>";

/***/ }),

/***/ "./style/img/settings.svg":
/*!********************************!*\
  !*** ./style/img/settings.svg ***!
  \********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"currentColor\" height=\"54\" width=\"54\" class=\"bi bi-play-fill\" viewBox=\"0 0 54 54\">\n\t<path d=\"M51.22,21h-5.052c-0.812,0-1.481-0.447-1.792-1.197s-0.153-1.54,0.42-2.114l3.572-3.571   c0.525-0.525,0.814-1.224,0.814-1.966c0-0.743-0.289-1.441-0.814-1.967l-4.553-4.553c-1.05-1.05-2.881-1.052-3.933,0l-3.571,3.571   c-0.574,0.573-1.366,0.733-2.114,0.421C33.447,9.313,33,8.644,33,7.832V2.78C33,1.247,31.753,0,30.22,0H23.78   C22.247,0,21,1.247,21,2.78v5.052c0,0.812-0.447,1.481-1.197,1.792c-0.748,0.313-1.54,0.152-2.114-0.421l-3.571-3.571   c-1.052-1.052-2.883-1.05-3.933,0l-4.553,4.553c-0.525,0.525-0.814,1.224-0.814,1.967c0,0.742,0.289,1.44,0.814,1.966l3.572,3.571   c0.573,0.574,0.73,1.364,0.42,2.114S8.644,21,7.832,21H2.78C1.247,21,0,22.247,0,23.78v6.439C0,31.753,1.247,33,2.78,33h5.052   c0.812,0,1.481,0.447,1.792,1.197s0.153,1.54-0.42,2.114l-3.572,3.571c-0.525,0.525-0.814,1.224-0.814,1.966   c0,0.743,0.289,1.441,0.814,1.967l4.553,4.553c1.051,1.051,2.881,1.053,3.933,0l3.571-3.572c0.574-0.573,1.363-0.731,2.114-0.42   c0.75,0.311,1.197,0.98,1.197,1.792v5.052c0,1.533,1.247,2.78,2.78,2.78h6.439c1.533,0,2.78-1.247,2.78-2.78v-5.052   c0-0.812,0.447-1.481,1.197-1.792c0.751-0.312,1.54-0.153,2.114,0.42l3.571,3.572c1.052,1.052,2.883,1.05,3.933,0l4.553-4.553   c0.525-0.525,0.814-1.224,0.814-1.967c0-0.742-0.289-1.44-0.814-1.966l-3.572-3.571c-0.573-0.574-0.73-1.364-0.42-2.114   S45.356,33,46.168,33h5.052c1.533,0,2.78-1.247,2.78-2.78V23.78C54,22.247,52.753,21,51.22,21z M52,30.22   C52,30.65,51.65,31,51.22,31h-5.052c-1.624,0-3.019,0.932-3.64,2.432c-0.622,1.5-0.295,3.146,0.854,4.294l3.572,3.571   c0.305,0.305,0.305,0.8,0,1.104l-4.553,4.553c-0.304,0.304-0.799,0.306-1.104,0l-3.571-3.572c-1.149-1.149-2.794-1.474-4.294-0.854   c-1.5,0.621-2.432,2.016-2.432,3.64v5.052C31,51.65,30.65,52,30.22,52H23.78C23.35,52,23,51.65,23,51.22v-5.052   c0-1.624-0.932-3.019-2.432-3.64c-0.503-0.209-1.021-0.311-1.533-0.311c-1.014,0-1.997,0.4-2.761,1.164l-3.571,3.572   c-0.306,0.306-0.801,0.304-1.104,0l-4.553-4.553c-0.305-0.305-0.305-0.8,0-1.104l3.572-3.571c1.148-1.148,1.476-2.794,0.854-4.294   C10.851,31.932,9.456,31,7.832,31H2.78C2.35,31,2,30.65,2,30.22V23.78C2,23.35,2.35,23,2.78,23h5.052   c1.624,0,3.019-0.932,3.64-2.432c0.622-1.5,0.295-3.146-0.854-4.294l-3.572-3.571c-0.305-0.305-0.305-0.8,0-1.104l4.553-4.553   c0.304-0.305,0.799-0.305,1.104,0l3.571,3.571c1.147,1.147,2.792,1.476,4.294,0.854C22.068,10.851,23,9.456,23,7.832V2.78   C23,2.35,23.35,2,23.78,2h6.439C30.65,2,31,2.35,31,2.78v5.052c0,1.624,0.932,3.019,2.432,3.64   c1.502,0.622,3.146,0.294,4.294-0.854l3.571-3.571c0.306-0.305,0.801-0.305,1.104,0l4.553,4.553c0.305,0.305,0.305,0.8,0,1.104   l-3.572,3.571c-1.148,1.148-1.476,2.794-0.854,4.294c0.621,1.5,2.016,2.432,3.64,2.432h5.052C51.65,23,52,23.35,52,23.78V30.22z\"/>\n\t<path d=\"M27,18c-4.963,0-9,4.037-9,9s4.037,9,9,9s9-4.037,9-9S31.963,18,27,18z M27,34c-3.859,0-7-3.141-7-7s3.141-7,7-7   s7,3.141,7,7S30.859,34,27,34z\"/>\n</svg>";

/***/ }),

/***/ "./style/img/stop.svg":
/*!****************************!*\
  !*** ./style/img/stop.svg ***!
  \****************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"currentColor\" class=\"bi bi-stop-circle\" viewBox=\"0 0 16 16\">\n  <path d=\"M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z\"/>\n  <path d=\"M5 6.5A1.5 1.5 0 0 1 6.5 5h3A1.5 1.5 0 0 1 11 6.5v3A1.5 1.5 0 0 1 9.5 11h-3A1.5 1.5 0 0 1 5 9.5v-3z\"/>\n</svg>";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%272%27 fill=%27%23fff%27/%3e%3c/svg%3e":
/*!******************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%272%27 fill=%27%23fff%27/%3e%3c/svg%3e ***!
  \******************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%272%27 fill=%27%23fff%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%2386b7fe%27/%3e%3c/svg%3e":
/*!*********************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%2386b7fe%27/%3e%3c/svg%3e ***!
  \*********************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%2386b7fe%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%23fff%27/%3e%3c/svg%3e":
/*!******************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%23fff%27/%3e%3c/svg%3e ***!
  \******************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%23fff%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%280, 0, 0, 0.25%29%27/%3e%3c/svg%3e":
/*!***********************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%280, 0, 0, 0.25%29%27/%3e%3c/svg%3e ***!
  \***********************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%280, 0, 0, 0.25%29%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%28255, 255, 255, 0.25%29%27/%3e%3c/svg%3e":
/*!*****************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%28255, 255, 255, 0.25%29%27/%3e%3c/svg%3e ***!
  \*****************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%28255, 255, 255, 0.25%29%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 12 12%27 width=%2712%27 height=%2712%27 fill=%27none%27 stroke=%27%23dc3545%27%3e%3ccircle cx=%276%27 cy=%276%27 r=%274.5%27/%3e%3cpath stroke-linejoin=%27round%27 d=%27M5.8 3.6h.4L6 6.5z%27/%3e%3ccircle cx=%276%27 cy=%278.2%27 r=%27.6%27 fill=%27%23dc3545%27 stroke=%27none%27/%3e%3c/svg%3e":
/*!*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 12 12%27 width=%2712%27 height=%2712%27 fill=%27none%27 stroke=%27%23dc3545%27%3e%3ccircle cx=%276%27 cy=%276%27 r=%274.5%27/%3e%3cpath stroke-linejoin=%27round%27 d=%27M5.8 3.6h.4L6 6.5z%27/%3e%3ccircle cx=%276%27 cy=%278.2%27 r=%27.6%27 fill=%27%23dc3545%27 stroke=%27none%27/%3e%3c/svg%3e ***!
  \*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 12 12%27 width=%2712%27 height=%2712%27 fill=%27none%27 stroke=%27%23dc3545%27%3e%3ccircle cx=%276%27 cy=%276%27 r=%274.5%27/%3e%3cpath stroke-linejoin=%27round%27 d=%27M5.8 3.6h.4L6 6.5z%27/%3e%3ccircle cx=%276%27 cy=%278.2%27 r=%27.6%27 fill=%27%23dc3545%27 stroke=%27none%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23000%27%3e%3cpath d=%27M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414z%27/%3e%3c/svg%3e":
/*!**************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23000%27%3e%3cpath d=%27M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414z%27/%3e%3c/svg%3e ***!
  \**************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23000%27%3e%3cpath d=%27M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414z%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%236ea8fe%27%3e%3cpath fill-rule=%27evenodd%27 d=%27M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z%27/%3e%3c/svg%3e":
/*!****************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%236ea8fe%27%3e%3cpath fill-rule=%27evenodd%27 d=%27M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z%27/%3e%3c/svg%3e ***!
  \****************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%236ea8fe%27%3e%3cpath fill-rule=%27evenodd%27 d=%27M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z%27/%3e%3c/svg%3e":
/*!************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z%27/%3e%3c/svg%3e ***!
  \************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z%27/%3e%3c/svg%3e":
/*!*************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z%27/%3e%3c/svg%3e ***!
  \*************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23052c65%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27M2 5L8 11L14 5%27/%3e%3c/svg%3e":
/*!*********************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23052c65%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27M2 5L8 11L14 5%27/%3e%3c/svg%3e ***!
  \*********************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23052c65%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27M2 5L8 11L14 5%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23212529%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27M2 5L8 11L14 5%27/%3e%3c/svg%3e":
/*!*********************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23212529%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27M2 5L8 11L14 5%27/%3e%3c/svg%3e ***!
  \*********************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23212529%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27M2 5L8 11L14 5%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23343a40%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e":
/*!****************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23343a40%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e ***!
  \****************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23343a40%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23dee2e6%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e":
/*!****************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23dee2e6%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e ***!
  \****************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23dee2e6%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27M6 10h8%27/%3e%3c/svg%3e":
/*!********************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27M6 10h8%27/%3e%3c/svg%3e ***!
  \********************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27M6 10h8%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27m6 10 3 3 6-6%27/%3e%3c/svg%3e":
/*!**************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27m6 10 3 3 6-6%27/%3e%3c/svg%3e ***!
  \**************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27m6 10 3 3 6-6%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%28255, 255, 255, 0.55%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e":
/*!******************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%28255, 255, 255, 0.55%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e ***!
  \******************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%28255, 255, 255, 0.55%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%2833, 37, 41, 0.75%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e":
/*!***************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%2833, 37, 41, 0.75%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e ***!
  \***************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%2833, 37, 41, 0.75%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 8 8%27%3e%3cpath fill=%27%23198754%27 d=%27M2.3 6.73.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1z%27/%3e%3c/svg%3e":
/*!**********************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 8 8%27%3e%3cpath fill=%27%23198754%27 d=%27M2.3 6.73.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1z%27/%3e%3c/svg%3e ***!
  \**********************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 8 8%27%3e%3cpath fill=%27%23198754%27 d=%27M2.3 6.73.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1z%27/%3e%3c/svg%3e";

/***/ })

}]);
//# sourceMappingURL=lib_index_js-data_image_svg_xml_3csvg_xmlns_27http_www_w3_org_2000_svg_27_viewBox_27-4_-4_8_8-8bf12d.6acb5054291f75777f25.js.map
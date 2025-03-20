"use strict";
(self["webpackChunkenverge_placeholder"] = self["webpackChunkenverge_placeholder"] || []).push([["lib_index_js"],{

/***/ "./lib/components/CountdownTimer.js":
/*!******************************************!*\
  !*** ./lib/components/CountdownTimer.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CountdownTimer: () => (/* binding */ CountdownTimer)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const CountdownTimer = () => {
    const [timeLeft, setTimeLeft] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({
        hours: 16,
        minutes: 12,
        seconds: 30
    });
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const interval = setInterval(() => {
            setTimeLeft(prev => {
                let newSeconds = prev.seconds - 1;
                let newMinutes = prev.minutes;
                let newHours = prev.hours;
                if (newSeconds < 0) {
                    newSeconds = 59;
                    newMinutes -= 1;
                }
                if (newMinutes < 0) {
                    newMinutes = 59;
                    newHours -= 1;
                }
                if (newHours < 0) {
                    clearInterval(interval);
                    return prev;
                }
                return {
                    hours: newHours,
                    minutes: newMinutes,
                    seconds: newSeconds
                };
            });
        }, 1000);
        return () => clearInterval(interval);
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, "Our runtime is experiencing high demand."),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null,
            "Your process will execute in",
            ' ',
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { fontWeight: 'bold' } },
                timeLeft.hours,
                "hours ",
                timeLeft.minutes,
                "minutes and ",
                timeLeft.seconds,
                "seconds"))));
};


/***/ }),

/***/ "./lib/components/EnergyMixBar.js":
/*!****************************************!*\
  !*** ./lib/components/EnergyMixBar.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   EnergyMixBar: () => (/* binding */ EnergyMixBar)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const EnergyMixBar = () => {
    const [isDark, setIsDark] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [energyMix, setEnergyMix] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({
        solar: 40,
        wind: 30,
        battery: 25,
        grid: 5
    });
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        var _a;
        // Theme management
        const themeManager = (_a = window.jupyterlab) === null || _a === void 0 ? void 0 : _a.themeManager;
        const updateTheme = () => {
            setIsDark(!(themeManager === null || themeManager === void 0 ? void 0 : themeManager.isLight(themeManager === null || themeManager === void 0 ? void 0 : themeManager.theme)));
        };
        if (themeManager) {
            updateTheme();
            themeManager.themeChanged.connect(updateTheme);
            return () => themeManager.themeChanged.disconnect(updateTheme);
        }
    }, []);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        // Energy mix animation
        const updateValues = () => {
            setEnergyMix(prev => {
                // Generate random fluctuations between -2.5% and +2.5%
                const fluctuate = () => (Math.random() - 0.5) * 5;
                // Calculate new values with fluctuations
                let newSolar = Math.max(35, Math.min(45, prev.solar + fluctuate()));
                let newWind = Math.max(25, Math.min(35, prev.wind + fluctuate()));
                let newBattery = Math.max(20, Math.min(30, prev.battery + fluctuate()));
                let newGrid = Math.max(2, Math.min(5, prev.grid + fluctuate()));
                // Normalize to ensure total is 100%
                const total = newSolar + newWind + newBattery + newGrid;
                const scale = 100 / total;
                return {
                    solar: Math.round(newSolar * scale * 10) / 10,
                    wind: Math.round(newWind * scale * 10) / 10,
                    battery: Math.round(newBattery * scale * 10) / 10,
                    grid: Math.round(newGrid * scale * 10) / 10
                };
            });
        };
        const interval = setInterval(updateValues, 2000);
        return () => clearInterval(interval);
    }, []);
    const colors = {
        solar: isDark ? '#FFD700' : '#FFB84D',
        wind: isDark ? '#87CEFA' : '#5B9FFF',
        battery: isDark ? '#DA70D6' : '#B57EDC',
        grid: isDark ? '#FF4444' : '#FF6B6B'
    };
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: {
            display: 'flex',
            alignItems: 'center',
            marginLeft: '20px',
        } },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: {
                display: 'flex',
                alignItems: 'center',
                height: '20px',
                width: '200px',
                border: '1px solid var(--jp-border-color1)',
                borderRadius: '4px',
                overflow: 'hidden'
            } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { width: `${energyMix.solar}%`, height: '100%', backgroundColor: colors.solar }, title: `Solar: ${energyMix.solar}%` }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { width: `${energyMix.wind}%`, height: '100%', backgroundColor: colors.wind }, title: `Wind: ${energyMix.wind}%` }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { width: `${energyMix.battery}%`, height: '100%', backgroundColor: colors.battery }, title: `Battery: ${energyMix.battery}%` }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { width: `${energyMix.grid}%`, height: '100%', backgroundColor: colors.grid }, title: `Grid: ${energyMix.grid}%` })),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: {
                marginLeft: '10px',
                fontSize: '12px',
                display: 'flex',
                gap: '8px'
            } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { color: 'var(--jp-ui-font-color1)' } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { color: colors.solar } }, "\u25A0"),
                " Solar ",
                energyMix.solar,
                "%"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { color: 'var(--jp-ui-font-color1)' } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { color: colors.wind } }, "\u25A0"),
                " Wind ",
                energyMix.wind,
                "%"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { color: 'var(--jp-ui-font-color1)' } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { color: colors.battery } }, "\u25A0"),
                " Battery ",
                energyMix.battery,
                "%"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { color: 'var(--jp-ui-font-color1)' } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { color: colors.grid } }, "\u25A0"),
                " Grid ",
                energyMix.grid,
                "%"))));
};


/***/ }),

/***/ "./lib/components/SidePanel.js":
/*!*************************************!*\
  !*** ./lib/components/SidePanel.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createSidePanel: () => (/* binding */ createSidePanel)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

const createSidePanel = (toggleId) => {
    const sidePanel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
    sidePanel.id = 'enverge-placeholder-panel';
    sidePanel.title.label = 'Enverge Stats';
    sidePanel.title.closable = true;
    sidePanel.node.innerHTML = `
    <div style="padding: 16px">
      <div style="
        background: var(--jp-layout-color2);
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 24px;
        border-left: 4px solid var(--jp-brand-color1);
      ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <h3 style="margin: 0; font-size: 16px; color: var(--jp-ui-font-color0);">GPU Status:</h3>
          <span id="gpu-usage-status" style="
            font-weight: 500; 
            font-size: 16px;
            padding: 4px 10px;
            background: var(--jp-layout-color3);
            border-radius: 4px;
            color: var(--jp-ui-font-color1);
          ">No GPU used</span>
        </div>
      </div>

      <div style="margin-bottom: 24px">
        <h3 style="margin: 0 0 16px 0">GPU Configuration</h3>
        <div style="
          display: flex;
          align-items: center;
          gap: 12px;
        ">
          <span>Type:</span>
          <select style="
            padding: 6px 12px;
            border-radius: 4px;
            border: 1px solid var(--jp-border-color1);
            background: var(--jp-layout-color1);
            color: var(--jp-ui-font-color1);
            min-width: 150px;
          ">
            <option value="H200" selected>H200 (141GB)</option>
            <option value="A100" disabled>A100 (80GB)</option>
            <option value="L4" disabled>L4 (24GB)</option>
            <option value="T4" disabled>T4 (16GB)</option>
          </select>
        </div>
      </div>

      <div style="margin-bottom: 24px">
        <div style="
          background: var(--jp-layout-color2);
          padding: 20px;
          border-radius: 8px;
        ">
          <h3 style="margin: 0 0 16px 0">GPU Details</h3>
          <div style="display: flex; justify-content: space-between; margin-bottom: 12px">
            <span>Model:</span>
            <span style="font-weight: 500">NVIDIA H200</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 12px">
            <span>GPU Load:</span>
            <span id="gpu-load-value" style="font-weight: 500">0%</span>
          </div>
          <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
              <span>Memory Usage:</span>
              <span id="memory-usage-value" style="font-weight: 500">0GB / 141GB (0%)</span>
            </div>
            <div style="
              width: 100%;
              height: 8px;
              background: var(--jp-layout-color3);
              border-radius: 4px;
              overflow: hidden;
            ">
              <div id="memory-usage-bar" style="
                width: 0%;
                height: 100%;
                background: var(--jp-brand-color1);
                border-radius: 4px;
              "></div>
            </div>
          </div>
        </div>
      </div>

      <div style="
        background: var(--jp-layout-color2);
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 24px;
      ">
        <h3 style="margin: 0 0 12px 0">Credit Status</h3>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
          <span>Available Credits:</span>
          <span id="available-credits" style="font-weight: bold">100 hours 0 min ($300)</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
          <span>Credit Usage Rate:</span>
          <span>$3/hour (H200 GPU)</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <span>Auto-reload at:</span>
          <span>25 hours remaining</span>
        </div>
      </div>

      <div style="margin-bottom: 24px">
        <h3 style="margin: 0 0 12px 0">Usage Statistics</h3>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
          <span>Today's GPU Time:</span>
          <span id="today-usage">4 hours 30 min</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
          <span>This Week:</span>
          <span>14 hours 12 min</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <span>This Month:</span>
          <span>45 hours 48 min</span>
        </div>
      </div>

      <div style="margin-bottom: 24px">
        <h3 style="margin: 0 0 12px 0">Energy Stats</h3>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
          <span>Current Power:</span>
          <span>2.5 kW</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <span>Daily Usage:</span>
          <span>45 kWh</span>
        </div>
      </div>

      <label>
        <input type="checkbox" id="${toggleId}"> Simulate Congestion
      </label>
    </div>
  `;
    return sidePanel;
};


/***/ }),

/***/ "./lib/components/ThemeSwitch.js":
/*!***************************************!*\
  !*** ./lib/components/ThemeSwitch.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ThemeSwitch: () => (/* binding */ ThemeSwitch)
/* harmony export */ });
/* harmony import */ var _jupyter_react_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter/react-components */ "webpack/sharing/consume/default/@jupyter/react-components");
/* harmony import */ var _jupyter_react_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_react_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);



const ThemeSwitch = (props) => {
    const { themeManager, onChange, ...others } = props;
    const [dark, setDark] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const updateChecked = () => {
        const isDark = !themeManager.isLight(themeManager.theme);
        setDark(!!isDark);
    };
    const handleChange = (event) => {
        if (onChange) {
            onChange(event);
        }
    };
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        let timeout = 0;
        if (!themeManager.theme) {
            // TODO: investigate why the themeManager is undefined
            timeout = setTimeout(() => {
                updateChecked();
            }, 500);
        }
        else {
            updateChecked();
        }
        themeManager.themeChanged.connect(updateChecked);
        return () => {
            clearTimeout(timeout);
            themeManager.themeChanged.disconnect(updateChecked);
        };
    });
    return react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyter_react_components__WEBPACK_IMPORTED_MODULE_0__.Switch, { ...others, onChange: handleChange, "aria-checked": dark });
};


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
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _components_ThemeSwitch__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/ThemeSwitch */ "./lib/components/ThemeSwitch.js");
/* harmony import */ var _components_EnergyMixBar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/EnergyMixBar */ "./lib/components/EnergyMixBar.js");
/* harmony import */ var _components_CountdownTimer__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/CountdownTimer */ "./lib/components/CountdownTimer.js");
/* harmony import */ var _components_SidePanel__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./components/SidePanel */ "./lib/components/SidePanel.js");
/* harmony import */ var _services_gpu_detection__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./services/gpu-detection */ "./lib/services/gpu-detection.js");
/* harmony import */ var _services_theme_manager__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./services/theme-manager */ "./lib/services/theme-manager.js");
/* harmony import */ var _services_credits_system__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./services/credits-system */ "./lib/services/credits-system.js");
/* harmony import */ var _utils_helpers__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./utils/helpers */ "./lib/utils/helpers.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");
/* harmony import */ var _style_enverge_svg__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../style/enverge.svg */ "./style/enverge.svg");






// Import components




// Import services



// Import utilities

// Import styles


// WARNING: this must match the name of the extension in the package.json
const placeholderPluginId = 'enverge_placeholder:plugin';
// Add GPU detection functionality to the extension
const extension = {
    id: placeholderPluginId,
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: async (app, themeManager, notebookTracker, toolbarRegistry, restorer) => {
        console.log('enverge-placeholder extension is activated!');
        // Setup theme management
        const toggleTheme = (0,_services_theme_manager__WEBPACK_IMPORTED_MODULE_10__.setupThemeManager)(app, themeManager);
        // Adjust UI for branding
        (0,_services_theme_manager__WEBPACK_IMPORTED_MODULE_10__.adjustUIForBranding)();
        // Replace logo and pass theme manager
        setTimeout(() => {
            (0,_services_theme_manager__WEBPACK_IMPORTED_MODULE_10__.replaceLogo)(_style_enverge_svg__WEBPACK_IMPORTED_MODULE_14__, themeManager);
            // Set up listener for theme changes
            (0,_services_theme_manager__WEBPACK_IMPORTED_MODULE_10__.setupLogoThemeListener)(themeManager);
        }, 2000);
        // Initialize credits display
        setTimeout(_services_credits_system__WEBPACK_IMPORTED_MODULE_11__.updateCreditsDisplay, 100);
        // Create toggle ID for congestion simulation
        const toggleId = 'cell-alert-toggle';
        // Create side panel
        const sidePanel = (0,_components_SidePanel__WEBPACK_IMPORTED_MODULE_8__.createSidePanel)(toggleId);
        // Add to right side panel
        app.shell.add(sidePanel, 'right');
        if (restorer) {
            restorer.add(sidePanel, sidePanel.id);
        }
        // Track the update interval
        let updateInterval = null;
        // Track the currently executing cell
        let currentExecutingCellId = null;
        // Unified function to update all GPU-related UI elements and stats
        const updateGPUState = (isGPUActive) => {
            // Update the GPU status display
            const gpuStatusElement = document.getElementById('gpu-usage-status');
            if (gpuStatusElement) {
                gpuStatusElement.textContent = isGPUActive ? 'GPU used now' : 'No GPU used';
                gpuStatusElement.style.color = isGPUActive
                    ? 'var(--jp-accent-color1)'
                    : 'var(--jp-ui-font-color1)';
            }
            // Update GPU stats (load, memory usage, credits)
            (0,_services_credits_system__WEBPACK_IMPORTED_MODULE_11__.updateGPUStats)(isGPUActive);
            // Manage the update interval
            if (isGPUActive) {
                // Clear any existing interval first to prevent duplicates
                if (updateInterval !== null) {
                    clearInterval(updateInterval);
                }
                // Set up periodic updates while GPU is active - use the current state
                updateInterval = window.setInterval(() => {
                    // Only update with active GPU if we still have an executing cell
                    const stillActive = currentExecutingCellId !== null;
                    (0,_services_credits_system__WEBPACK_IMPORTED_MODULE_11__.updateGPUStats)(stillActive);
                    // If no longer active, clear the interval
                    if (!stillActive && updateInterval !== null) {
                        clearInterval(updateInterval);
                        updateInterval = null;
                    }
                }, 2000);
            }
            else {
                // Clear the interval when GPU is no longer active
                if (updateInterval !== null) {
                    clearInterval(updateInterval);
                    updateInterval = null;
                }
            }
        };
        if (toolbarRegistry) {
            console.log('Adding widget to toolbar registry', { toolbarRegistry });
            toolbarRegistry.addFactory('TopBar', 'enverge-placeholder', () => {
                console.log('Creating enverge-placeholder widget');
                const widget = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", { style: { display: 'flex', alignItems: 'center' } },
                    react__WEBPACK_IMPORTED_MODULE_4__.createElement(_components_ThemeSwitch__WEBPACK_IMPORTED_MODULE_5__.ThemeSwitch, { themeManager: themeManager, onChange: () => toggleTheme() },
                        react__WEBPACK_IMPORTED_MODULE_4__.createElement("span", { slot: "unchecked-message" }, "Light"),
                        react__WEBPACK_IMPORTED_MODULE_4__.createElement("span", { slot: "checked-message" }, "Dark")),
                    react__WEBPACK_IMPORTED_MODULE_4__.createElement(_components_EnergyMixBar__WEBPACK_IMPORTED_MODULE_6__.EnergyMixBar, null)));
                return widget;
            });
        }
        else {
            console.error('toolbarRegistry not available');
        }
        // Clean up when notebook is closed or changed
        notebookTracker.currentChanged.connect((_, notebook) => {
            if (notebook) {
                console.log('Notebook changed, setting up GPU detection for:', notebook.title.label);
                // Clean up when notebook is closed or changed
                notebook.disposed.connect(() => {
                    console.log('Notebook disposed, clearing GPU tracking');
                    currentExecutingCellId = null;
                });
                // Clear tracking when the kernel is restarted
                notebook.sessionContext.kernelChanged.connect(() => {
                    console.log('Kernel changed or restarted, clearing GPU tracking');
                    currentExecutingCellId = null;
                });
                // Listen for kernel interruption
                notebook.sessionContext.statusChanged.connect((_, status) => {
                    console.log(`Kernel status changed to: ${status}`);
                    if (status === 'idle' && currentExecutingCellId) {
                        console.log('Kernel interrupted, clearing current cell tracking');
                        currentExecutingCellId = null;
                        // Update GPU state to show no GPU usage after kernel interruption
                        updateGPUState(false);
                    }
                });
                // Listen for cell execution starting
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.NotebookActions.executionScheduled.connect((_, args) => {
                    const { cell } = args;
                    console.log('Cell execution scheduled, cell ID:', cell.model.id);
                    // Get the cell's code
                    const code = cell.model.sharedModel.getSource();
                    // Generate a unique ID for this cell based on its content
                    const contentHash = (0,_utils_helpers__WEBPACK_IMPORTED_MODULE_12__.hashCode)(code);
                    const cellId = `${cell.model.id}-${contentHash}`;
                    console.log('Generated cell ID for execution:', cellId);
                    // Check if the code uses GPU
                    const usesGPU = (0,_services_gpu_detection__WEBPACK_IMPORTED_MODULE_9__.detectGPUUsage)(code);
                    console.log({ usesGPU });
                    if (usesGPU) {
                        console.log('GPU usage detected in cell');
                        // Set as current executing cell if it's a GPU cell
                        currentExecutingCellId = cellId;
                        console.log('Executing GPU cell, current executing cell set to:', currentExecutingCellId);
                        // Update GPU state to show GPU is active
                        updateGPUState(true);
                    }
                    else {
                        console.log('Executing non-GPU cell');
                        // Update GPU state to show no GPU usage
                        updateGPUState(false);
                    }
                    const toggle = document.getElementById(toggleId);
                    if (toggle === null || toggle === void 0 ? void 0 : toggle.checked) {
                        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title: 'Congestion Alert',
                            body: (react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", null,
                                react__WEBPACK_IMPORTED_MODULE_4__.createElement(_components_CountdownTimer__WEBPACK_IMPORTED_MODULE_7__.CountdownTimer, null),
                                react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", { style: { marginTop: '10px', marginBottom: '10px' } },
                                    react__WEBPACK_IMPORTED_MODULE_4__.createElement("label", null,
                                        "Purchase priority runtime (hours):",
                                        ' ',
                                        react__WEBPACK_IMPORTED_MODULE_4__.createElement("select", { defaultValue: "1" },
                                            react__WEBPACK_IMPORTED_MODULE_4__.createElement("option", { value: "1" }, "1 hour ($3)"),
                                            react__WEBPACK_IMPORTED_MODULE_4__.createElement("option", { value: "4" }, "4 hours ($12)"),
                                            react__WEBPACK_IMPORTED_MODULE_4__.createElement("option", { value: "8" }, "8 hours ($24)"),
                                            react__WEBPACK_IMPORTED_MODULE_4__.createElement("option", { value: "24" }, "24 hours ($150)")))),
                                react__WEBPACK_IMPORTED_MODULE_4__.createElement("button", { className: "jp-mod-styled", onClick: (e) => {
                                        e.preventDefault();
                                        const paymentArea = document.getElementById('payment-area');
                                        if (paymentArea) {
                                            paymentArea.style.display = 'block';
                                        }
                                    }, style: {
                                        width: '100%',
                                        padding: '10px',
                                        backgroundColor: 'var(--jp-brand-color1)',
                                        color: 'white',
                                        border: 'none',
                                        borderRadius: '4px',
                                        cursor: 'pointer',
                                        marginTop: '5px',
                                        marginBottom: '5px',
                                        lineHeight: '15px'
                                    } }, "Purchase Priority Runtime"),
                                react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", { id: "payment-area", style: {
                                        display: 'none',
                                        border: '1px solid var(--jp-border-color1)',
                                        borderRadius: '4px',
                                        padding: '15px',
                                        marginTop: '10px'
                                    } },
                                    react__WEBPACK_IMPORTED_MODULE_4__.createElement("input", { type: "text", placeholder: "Card number", style: {
                                            width: '100%',
                                            padding: '8px',
                                            marginBottom: '10px',
                                            border: '1px solid var(--jp-border-color1)',
                                            borderRadius: '4px'
                                        } }),
                                    react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", { style: { display: 'flex', gap: '10px', marginBottom: '10px' } },
                                        react__WEBPACK_IMPORTED_MODULE_4__.createElement("input", { type: "text", placeholder: "MM/YY", style: {
                                                width: '50%',
                                                padding: '8px',
                                                border: '1px solid var(--jp-border-color1)',
                                                borderRadius: '4px'
                                            } }),
                                        react__WEBPACK_IMPORTED_MODULE_4__.createElement("input", { type: "text", placeholder: "CVC", style: {
                                                width: '50%',
                                                padding: '8px',
                                                border: '1px solid var(--jp-border-color1)',
                                                borderRadius: '4px'
                                            } })),
                                    react__WEBPACK_IMPORTED_MODULE_4__.createElement("button", { className: "jp-mod-styled", onClick: () => {
                                            var _a, _b, _c;
                                            const cardNumber = (_a = document.querySelector('input[placeholder="Card number"]')) === null || _a === void 0 ? void 0 : _a.value;
                                            const expiry = (_b = document.querySelector('input[placeholder="MM/YY"]')) === null || _b === void 0 ? void 0 : _b.value;
                                            const cvc = (_c = document.querySelector('input[placeholder="CVC"]')) === null || _c === void 0 ? void 0 : _c.value;
                                            alert(`Card Details:\nNumber: ${cardNumber}\nExpiry: ${expiry}\nCVC: ${cvc}`);
                                        }, style: {
                                            width: '100%',
                                            padding: '10px',
                                            backgroundColor: 'var(--jp-brand-color1)',
                                            color: 'white',
                                            border: 'none',
                                            borderRadius: '4px',
                                            cursor: 'pointer',
                                            marginTop: '5px',
                                            marginBottom: '5px',
                                            lineHeight: '15px'
                                        } }, "Submit Payment")),
                                react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", { style: { marginTop: '10px', textAlign: 'right' } },
                                    react__WEBPACK_IMPORTED_MODULE_4__.createElement("a", { href: "https://docs.enverge.ai", target: "_blank", rel: "noopener noreferrer" }, "Click here to learn more")))),
                            buttons: [
                                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()
                            ]
                        });
                    }
                });
                // Reset stats after execution completes
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.NotebookActions.executed.connect((_, args) => {
                    console.log('Cell execution completed, cell ID:', args.cell.model.id);
                    // Clear the current executing cell ID when execution completes normally
                    if (currentExecutingCellId && args.cell.model.id === currentExecutingCellId.split('-')[0]) {
                        console.log('Clearing current executing cell ID after normal completion');
                        currentExecutingCellId = null;
                        // Update GPU state to show no GPU usage after execution completes
                        updateGPUState(false);
                    }
                });
            }
        });
        // Call this when a notebook is opened
        notebookTracker.currentChanged.connect(() => {
            (0,_services_gpu_detection__WEBPACK_IMPORTED_MODULE_9__.injectGPUMonitoring)(notebookTracker.currentWidget);
        });
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/services/credits-system.js":
/*!****************************************!*\
  !*** ./lib/services/credits-system.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   decreaseCredits: () => (/* binding */ decreaseCredits),
/* harmony export */   updateCreditsDisplay: () => (/* binding */ updateCreditsDisplay),
/* harmony export */   updateGPUStats: () => (/* binding */ updateGPUStats)
/* harmony export */ });
// Initialize credit state
const creditState = {
    availableCredits: {
        hours: 100,
        minutes: 0
    },
    usageStats: {
        today: 270, // 4.5 hours in minutes
        week: 852, // 14.2 hours in minutes
        month: 2748 // 45.8 hours in minutes
    }
};
// Function to update credits display in the UI
const updateCreditsDisplay = () => {
    const creditsElement = document.getElementById('available-credits');
    if (creditsElement) {
        const totalHours = creditState.availableCredits.hours + (creditState.availableCredits.minutes / 60);
        const dollarAmount = Math.round(totalHours * 3); // $3 per hour
        creditsElement.textContent = `${creditState.availableCredits.hours} hours ${creditState.availableCredits.minutes} min ($${dollarAmount})`;
    }
    // Update today's usage display
    const todayUsageElement = document.getElementById('today-usage');
    if (todayUsageElement) {
        const todayHours = Math.floor(creditState.usageStats.today / 60);
        const todayMinutes = creditState.usageStats.today % 60;
        todayUsageElement.textContent = `${todayHours} hours ${todayMinutes} min`;
    }
};
// Function to decrease credits by 1 minute
const decreaseCredits = () => {
    if (creditState.availableCredits.minutes > 0) {
        creditState.availableCredits.minutes -= 1;
    }
    else if (creditState.availableCredits.hours > 0) {
        creditState.availableCredits.hours -= 1;
        creditState.availableCredits.minutes = 59;
    }
    // Increase today's usage by 1 minute
    creditState.usageStats.today += 1;
    updateCreditsDisplay();
};
// Function to update GPU stats during cell execution
const updateGPUStats = (gpuUsageDetected = false) => {
    // Get the DOM elements
    const gpuLoadElement = document.getElementById('gpu-load-value');
    const memoryUsageElement = document.getElementById('memory-usage-value');
    const memoryUsageBar = document.getElementById('memory-usage-bar');
    // Update GPU stats based on usage detection
    if (gpuUsageDetected) {
        // Generate random GPU load between 85-98%
        const gpuLoad = Math.floor(Math.random() * 14) + 85;
        // Generate random memory usage between 80-95%
        const memoryPercentage = Math.floor(Math.random() * 16) + 80;
        const memoryGB = Math.round((memoryPercentage / 100) * 141);
        // Update the DOM elements with active GPU values
        if (gpuLoadElement) {
            gpuLoadElement.textContent = `${gpuLoad}%`;
        }
        if (memoryUsageElement) {
            memoryUsageElement.textContent = `${memoryGB}GB / 141GB (${memoryPercentage}%)`;
        }
        if (memoryUsageBar) {
            memoryUsageBar.style.width = `${memoryPercentage}%`;
        }
        // Always decrease credits when GPU is used
        decreaseCredits();
    }
    else {
        // Reset GPU stats to 0 when no GPU is used
        if (gpuLoadElement) {
            gpuLoadElement.textContent = '0%';
        }
        if (memoryUsageElement) {
            memoryUsageElement.textContent = '0GB / 141GB (0%)';
        }
        if (memoryUsageBar) {
            memoryUsageBar.style.width = '0%';
        }
    }
};


/***/ }),

/***/ "./lib/services/gpu-detection.js":
/*!***************************************!*\
  !*** ./lib/services/gpu-detection.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   detectGPUUsage: () => (/* binding */ detectGPUUsage),
/* harmony export */   injectGPUMonitoring: () => (/* binding */ injectGPUMonitoring)
/* harmony export */ });
// Function to detect GPU usage in code
const detectGPUUsage = (code) => {
    console.log('Checking for GPU usage in code...');
    // Pattern matching for common GPU usage in PyTorch
    const torchGPUPatterns = [
        /import torch/,
        /\.cuda\(\)/,
        /\.to\(['"]cuda['"]\)/,
        /\.to\(['"]mps['"]\)/, // Track an MPS for now too.
        /\.to\(device=['"]cuda['"]\)/,
        /torch\.cuda\./,
        /device\s*=\s*['"]cuda['"]/,
        /torch\.device\(['"]cuda['"]\)/
    ];
    // Pattern matching for TensorFlow GPU usage
    const tfGPUPatterns = [
        /import tensorflow/,
        /with tf\.device\(['"]\/GPU/,
        /tf\.config\.list_physical_devices\(['"]GPU['"]\)/
    ];
    // Pattern matching for JAX GPU usage
    const jaxGPUPatterns = [
        /import jax/,
        /jax\.device_put/,
        /jax\.devices\(\)/
    ];
    // Pattern matching for Hugging Face Transformers
    const transformersPatterns = [
        /from transformers import/,
        /Trainer\(/,
        /trainer\.train\(\)/,
        /training_args.*device/i,
        /TrainingArguments\(/
    ];
    // Check if any pattern matches
    const result = [...torchGPUPatterns, ...tfGPUPatterns, ...jaxGPUPatterns, ...transformersPatterns]
        .some(pattern => pattern.test(code));
    console.log({ result, code });
    console.log(`GPU usage detection result: ${result ? 'GPU usage detected' : 'No GPU usage detected'}`);
    return result;
};
// Function to inject GPU monitoring code into the kernel
const injectGPUMonitoring = async (notebook) => {
    var _a;
    if (!notebook)
        return;
    // Execute Python code in the kernel to set up monitoring
    const code = `
    import sys
    
    # Flag to track if GPU libraries are imported
    _gpu_libraries_imported = False
    
    # Original import function
    _original_import = __import__
    
    # Custom import hook to detect GPU libraries
    def _gpu_import_hook(name, *args, **kwargs):
        global _gpu_libraries_imported
        
        # Check for GPU-related libraries
        if name in ['torch', 'tensorflow', 'jax', 'cupy', 'transformers']:
            _gpu_libraries_imported = True
            
            # Additional checks for specific libraries
            if name == 'torch':
                # Check if CUDA is available
                exec('import torch; print("CUDA Available:", torch.cuda.is_available())')
            
            # Check for Hugging Face Transformers
            if name == 'transformers':
                try:
                    # Check if a GPU device is being used
                    exec('from transformers import TrainingArguments; print("Default device:", TrainingArguments(output_dir="./tmp").device)')
                except:
                    pass
            
        # Call the original import
        return _original_import(name, *args, **kwargs)
    
    # Replace the built-in import function
    sys.__import__ = _gpu_import_hook
    
    # Function to check GPU status
    def check_gpu_status():
        result = {"gpu_used": False, "memory_usage": 0, "library": None}
        
        if _gpu_libraries_imported:
            result["gpu_used"] = True
            
            # Try to get more detailed information based on available libraries
            try:
                import torch
                if torch.cuda.is_available():
                    result["library"] = "PyTorch"
                    result["memory_usage"] = torch.cuda.memory_allocated() / (1024**3)  # GB
            except:
                pass
                
            try:
                import tensorflow as tf
                gpus = tf.config.list_physical_devices('GPU')
                if gpus:
                    result["library"] = "TensorFlow"
                    # TF doesn't easily exposes memory usage
            except:
                pass
            
            try:
                import transformers
                result["library"] = "Transformers"
            except:
                pass
        
        return result
  `;
    // Execute this in the current notebook's kernel
    const session = notebook.sessionContext.session;
    await ((_a = session === null || session === void 0 ? void 0 : session.kernel) === null || _a === void 0 ? void 0 : _a.requestExecute({ code }).done);
};


/***/ }),

/***/ "./lib/services/theme-manager.js":
/*!***************************************!*\
  !*** ./lib/services/theme-manager.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   adjustUIForBranding: () => (/* binding */ adjustUIForBranding),
/* harmony export */   replaceLogo: () => (/* binding */ replaceLogo),
/* harmony export */   setupLogoThemeListener: () => (/* binding */ setupLogoThemeListener),
/* harmony export */   setupThemeManager: () => (/* binding */ setupThemeManager),
/* harmony export */   updateLogoColors: () => (/* binding */ updateLogoColors)
/* harmony export */ });
const setupThemeManager = (app, themeManager) => {
    const { commands } = app;
    const themes = [
        'JupyterLab Light',
        'Darcula',
    ];
    // Function to toggle between light and dark themes
    const toggleTheme = async () => {
        const isLight = themeManager.isLight(themeManager.theme);
        await commands.execute('apputils:change-theme', {
            theme: themes[~~isLight],
        });
    };
    return toggleTheme;
};
// Function to adjust UI elements for Enverge branding
const adjustUIForBranding = () => {
    // Adjust top panel height
    const adjustTopPanelHeight = () => {
        const topPanel = document.getElementById('jp-top-panel');
        const mainContentPanel = document.getElementById('jp-main-content-panel');
        if (topPanel) {
            topPanel.style.height = '46px';
        }
        if (mainContentPanel) {
            mainContentPanel.style.top = '46px';
        }
        const menuBar = document.getElementsByClassName('lm-MenuBar-content')[0];
        menuBar.style.paddingTop = '10px';
        const lmMenuBar = document.getElementsByClassName('lm-MenuBar');
        for (let i = 0; i < lmMenuBar.length; i++) {
            const element = lmMenuBar[i];
            element.style.color = 'var(--jp-accent-color1)';
        }
    };
    setTimeout(adjustTopPanelHeight, 2000);
};
// Function to replace the Jupyter logo with Enverge logo
const replaceLogo = (logoSvg, themeManager) => {
    console.log('replacing logo');
    const logoElement = document.getElementById('jp-MainLogo');
    if (logoElement && !logoElement.hasAttribute('data-replaced')) {
        // Set SVG directly as innerHTML
        logoElement.innerHTML = logoSvg;
        // Style the container
        logoElement.style.width = 'auto';
        logoElement.style.minWidth = 'max-content';
        logoElement.style.padding = '0 8px';
        // Find the SVG element we just inserted and style it
        const svgElement = logoElement.querySelector('svg');
        if (svgElement) {
            svgElement.style.height = '32px';
            svgElement.style.width = 'auto';
            // Apply theme-based color to the SVG text elements
            updateLogoColors(svgElement, themeManager);
        }
        logoElement.setAttribute('data-replaced', 'true');
    }
};
// Function to update logo colors based on theme
const updateLogoColors = (svgElement, themeManager) => {
    console.log('updating logo colors');
    const isDarkTheme = themeManager ? !themeManager.isLight(themeManager.theme) : false;
    // Set colors based on theme
    const textColor = isDarkTheme ? 'white' : '#333333';
    // Update text paths (the ENVERGE letters)
    // Get all paths within the specific transform group, regardless of current fill color
    const textPaths = svgElement.querySelectorAll('g[transform*="matrix(1,0,0,1"] path');
    textPaths.forEach(element => {
        const style = element.getAttribute('style');
        if (style) {
            // Replace any fill color with the new color
            const newStyle = style.replace(/fill:(#[0-9a-fA-F]{3,6}|white|black)/, `fill:${textColor}`);
            element.setAttribute('style', newStyle);
        }
    });
    // Update the hexagon stroke color
    // Get the hexagon path regardless of current stroke color
    const hexagonPath = svgElement.querySelector('g[transform*="matrix(0.1742"] path');
    if (hexagonPath) {
        const style = hexagonPath.getAttribute('style');
        if (style) {
            // Replace any stroke color with the new color
            const newStyle = style.replace(/stroke:(#[0-9a-fA-F]{3,6}|white|black)/, `stroke:${textColor}`);
            hexagonPath.setAttribute('style', newStyle);
        }
    }
};
// Function to listen for theme changes and update logo colors
const setupLogoThemeListener = (themeManager) => {
    themeManager.themeChanged.connect(() => {
        const logoElement = document.getElementById('jp-MainLogo');
        if (logoElement && logoElement.hasAttribute('data-replaced')) {
            const svgElement = logoElement.querySelector('svg');
            if (svgElement) {
                updateLogoColors(svgElement, themeManager);
            }
        }
    });
};


/***/ }),

/***/ "./lib/utils/helpers.js":
/*!******************************!*\
  !*** ./lib/utils/helpers.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   hashCode: () => (/* binding */ hashCode)
/* harmony export */ });
// Simple string hash function
function hashCode(str) {
    let hash = 0;
    if (str.length === 0)
        return hash.toString();
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash.toString();
}


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/* To increase the slider size */
.jp-Toolbar .jp-Toolbar-item {
  --density: 0;
}

`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA,gCAAgC;AAChC;EACE,YAAY;AACd","sourcesContent":["/* To increase the slider size */\n.jp-Toolbar .jp-Toolbar-item {\n  --density: 0;\n}\n\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `
`, "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/enverge.svg":
/*!***************************!*\
  !*** ./style/enverge.svg ***!
  \***************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n<svg width=\"100%\" height=\"100%\" viewBox=\"0 0 900 300\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\" xmlns:serif=\"http://www.serif.com/\" style=\"fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:1;\">\n    <g transform=\"matrix(1,0,0,1,-1.92771,2.29607)\">\n        <g>\n            <g transform=\"matrix(1.14531,0,0,1.14531,-12.8637,-1.46957)\">\n                <g transform=\"matrix(1,0,0,1,269.9,181.693)\">\n                    <g>\n                        <g>\n                            <path d=\"M11.521,0L11.521,-97.458L24.708,-97.458L24.708,0L11.521,0ZM20.5,0L20.5,-12.083L76.396,-12.083L76.396,0L20.5,0ZM20.5,-44.083L20.5,-55.604L71.75,-55.604L71.75,-44.083L20.5,-44.083ZM20.5,-85.375L20.5,-97.458L75.688,-97.458L75.688,-85.375L20.5,-85.375Z\" style=\"fill:white;fill-rule:nonzero;\"/>\n                        </g>\n                    </g>\n                </g>\n                <g transform=\"matrix(1,0,0,1,350.362,181.693)\">\n                    <g>\n                        <g>\n                            <path d=\"M56.438,0L56.438,-38.896C56.438,-43.948 54.844,-48.115 51.667,-51.396C48.484,-54.672 44.365,-56.312 39.313,-56.312C35.948,-56.312 32.958,-55.562 30.333,-54.062C27.708,-52.562 25.646,-50.5 24.146,-47.875C22.646,-45.26 21.896,-42.271 21.896,-38.896L16.708,-41.854C16.708,-46.896 17.833,-51.38 20.083,-55.312C22.333,-59.255 25.464,-62.375 29.479,-64.667C33.505,-66.958 38.047,-68.104 43.104,-68.104C48.156,-68.104 52.63,-66.839 56.521,-64.312C60.406,-61.781 63.469,-58.484 65.708,-54.417C67.958,-50.344 69.083,-46.01 69.083,-41.417L69.083,0L56.438,0ZM9.271,0L9.271,-66.708L21.896,-66.708L21.896,0L9.271,0Z\" style=\"fill:white;fill-rule:nonzero;\"/>\n                        </g>\n                    </g>\n                </g>\n                <g transform=\"matrix(1,0,0,1,424.927,181.693)\">\n                    <g>\n                        <g>\n                            <path d=\"M32.146,0L1.542,-66.708L15.583,-66.708L40.167,-10.396L32.021,-10.396L56.729,-66.708L70.208,-66.708L39.604,0L32.146,0Z\" style=\"fill:white;fill-rule:nonzero;\"/>\n                        </g>\n                    </g>\n                </g>\n                <g transform=\"matrix(1,0,0,1,494.296,181.693)\">\n                    <g>\n                        <g>\n                            <path d=\"M40.167,1.396C33.51,1.396 27.521,-0.125 22.188,-3.167C16.854,-6.208 12.635,-10.344 9.542,-15.583C6.458,-20.833 4.917,-26.776 4.917,-33.417C4.917,-39.969 6.438,-45.865 9.479,-51.104C12.521,-56.354 16.635,-60.5 21.833,-63.542C27.026,-66.583 32.854,-68.104 39.313,-68.104C45.49,-68.104 50.943,-66.698 55.667,-63.896C60.401,-61.089 64.104,-57.198 66.771,-52.229C69.438,-47.271 70.771,-41.651 70.771,-35.375C70.771,-34.443 70.719,-33.437 70.625,-32.354C70.526,-31.281 70.339,-30.047 70.063,-28.646L13.771,-28.646L13.771,-39.167L63.333,-39.167L58.688,-35.104C58.688,-39.604 57.885,-43.417 56.292,-46.542C54.708,-49.677 52.464,-52.109 49.563,-53.833C46.656,-55.568 43.151,-56.437 39.042,-56.437C34.734,-56.437 30.943,-55.5 27.667,-53.625C24.385,-51.76 21.859,-49.146 20.083,-45.771C18.302,-42.406 17.417,-38.427 17.417,-33.833C17.417,-29.151 18.344,-25.052 20.208,-21.542C22.083,-18.042 24.75,-15.333 28.208,-13.417C31.677,-11.5 35.667,-10.542 40.167,-10.542C43.901,-10.542 47.339,-11.193 50.479,-12.5C53.615,-13.802 56.313,-15.771 58.563,-18.396L66.708,-10.104C63.51,-6.365 59.594,-3.51 54.958,-1.542C50.333,0.417 45.401,1.396 40.167,1.396Z\" style=\"fill:white;fill-rule:nonzero;\"/>\n                        </g>\n                    </g>\n                </g>\n                <g transform=\"matrix(1,0,0,1,567.175,181.693)\">\n                    <g>\n                        <g>\n                            <path d=\"M9.271,0L9.271,-66.708L21.896,-66.708L21.896,0L9.271,0ZM21.896,-38.062L17.125,-40.167C17.125,-48.677 19.089,-55.464 23.021,-60.521C26.948,-65.573 32.615,-68.104 40.021,-68.104C43.396,-68.104 46.438,-67.51 49.146,-66.333C51.854,-65.167 54.38,-63.229 56.729,-60.521L48.438,-51.958C47.031,-53.458 45.49,-54.531 43.813,-55.187C42.13,-55.839 40.167,-56.167 37.917,-56.167C33.234,-56.167 29.396,-54.667 26.396,-51.667C23.396,-48.677 21.896,-44.146 21.896,-38.062Z\" style=\"fill:white;fill-rule:nonzero;\"/>\n                        </g>\n                    </g>\n                </g>\n                <g transform=\"matrix(1,0,0,1,623.625,181.693)\">\n                    <g>\n                        <g>\n                            <path d=\"M36.938,29.354C30.104,29.354 24.042,28.089 18.75,25.562C13.458,23.031 9.219,19.469 6.042,14.875L14.188,6.604C16.896,10.062 20.115,12.698 23.854,14.521C27.604,16.354 32.052,17.271 37.208,17.271C44.042,17.271 49.443,15.464 53.417,11.854C57.401,8.255 59.396,3.417 59.396,-2.667L59.396,-19.229L61.646,-34.271L59.396,-49.146L59.396,-66.708L72.042,-66.708L72.042,-2.667C72.042,3.693 70.563,9.26 67.604,14.042C64.656,18.818 60.542,22.562 55.25,25.271C49.958,27.99 43.854,29.354 36.938,29.354ZM36.938,-1.125C30.854,-1.125 25.396,-2.573 20.563,-5.479C15.74,-8.38 11.927,-12.38 9.125,-17.479C6.318,-22.573 4.917,-28.312 4.917,-34.687C4.917,-41.047 6.318,-46.729 9.125,-51.729C11.927,-56.74 15.74,-60.719 20.563,-63.667C25.396,-66.625 30.854,-68.104 36.938,-68.104C42.172,-68.104 46.802,-67.068 50.833,-65C54.859,-62.943 58.063,-60.068 60.438,-56.375C62.823,-52.677 64.115,-48.354 64.313,-43.396L64.313,-25.687C64.031,-20.823 62.698,-16.542 60.313,-12.833C57.922,-9.135 54.714,-6.26 50.688,-4.208C46.656,-2.151 42.073,-1.125 36.938,-1.125ZM39.458,-13.062C43.583,-13.062 47.208,-13.948 50.333,-15.729C53.469,-17.505 55.88,-20.005 57.563,-23.229C59.255,-26.464 60.104,-30.234 60.104,-34.542C60.104,-38.844 59.234,-42.609 57.5,-45.833C55.76,-49.068 53.354,-51.594 50.271,-53.417C47.188,-55.25 43.531,-56.167 39.313,-56.167C35.104,-56.167 31.406,-55.25 28.229,-53.417C25.047,-51.594 22.542,-49.068 20.708,-45.833C18.885,-42.609 17.979,-38.896 17.979,-34.687C17.979,-30.464 18.885,-26.714 20.708,-23.437C22.542,-20.172 25.068,-17.625 28.292,-15.792C31.526,-13.969 35.25,-13.062 39.458,-13.062Z\" style=\"fill:white;fill-rule:nonzero;\"/>\n                        </g>\n                    </g>\n                </g>\n                <g transform=\"matrix(1,0,0,1,702.543,181.693)\">\n                    <g>\n                        <g>\n                            <path d=\"M40.167,1.396C33.51,1.396 27.521,-0.125 22.188,-3.167C16.854,-6.208 12.635,-10.344 9.542,-15.583C6.458,-20.833 4.917,-26.776 4.917,-33.417C4.917,-39.969 6.438,-45.865 9.479,-51.104C12.521,-56.354 16.635,-60.5 21.833,-63.542C27.026,-66.583 32.854,-68.104 39.313,-68.104C45.49,-68.104 50.943,-66.698 55.667,-63.896C60.401,-61.089 64.104,-57.198 66.771,-52.229C69.438,-47.271 70.771,-41.651 70.771,-35.375C70.771,-34.443 70.719,-33.437 70.625,-32.354C70.526,-31.281 70.339,-30.047 70.063,-28.646L13.771,-28.646L13.771,-39.167L63.333,-39.167L58.688,-35.104C58.688,-39.604 57.885,-43.417 56.292,-46.542C54.708,-49.677 52.464,-52.109 49.563,-53.833C46.656,-55.568 43.151,-56.437 39.042,-56.437C34.734,-56.437 30.943,-55.5 27.667,-53.625C24.385,-51.76 21.859,-49.146 20.083,-45.771C18.302,-42.406 17.417,-38.427 17.417,-33.833C17.417,-29.151 18.344,-25.052 20.208,-21.542C22.083,-18.042 24.75,-15.333 28.208,-13.417C31.677,-11.5 35.667,-10.542 40.167,-10.542C43.901,-10.542 47.339,-11.193 50.479,-12.5C53.615,-13.802 56.313,-15.771 58.563,-18.396L66.708,-10.104C63.51,-6.365 59.594,-3.51 54.958,-1.542C50.333,0.417 45.401,1.396 40.167,1.396Z\" style=\"fill:white;fill-rule:nonzero;\"/>\n                        </g>\n                    </g>\n                </g>\n            </g>\n            <g transform=\"matrix(0.1742,0,0,0.1742,0.84694,22.2798)\">\n                <path d=\"M720.009,161.649L1203.52,440.834L1203.52,999.168L720.009,1278.35L236.462,999.168L236.462,440.834L720.009,161.649Z\" style=\"fill:none;fill-rule:nonzero;stroke:white;stroke-width:147.75px;\"/>\n            </g>\n        </g>\n    </g>\n</svg>\n";

/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.f2871af81acd6f429826.js.map
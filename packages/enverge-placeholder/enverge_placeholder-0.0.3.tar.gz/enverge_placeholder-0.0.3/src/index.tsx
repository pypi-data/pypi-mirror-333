import { JupyterFrontEnd, JupyterFrontEndPlugin, ILayoutRestorer } from '@jupyterlab/application';
import { IThemeManager, IToolbarWidgetRegistry, showDialog } from '@jupyterlab/apputils';
import { ReactWidget } from '@jupyterlab/ui-components';
import { INotebookTracker, NotebookActions } from '@jupyterlab/notebook';
import { Dialog } from '@jupyterlab/apputils';
import * as React from 'react';

// Import components
import { ThemeSwitch } from './components/ThemeSwitch';
import { EnergyMixBar } from './components/EnergyMixBar';
import { CountdownTimer } from './components/CountdownTimer';
import { createSidePanel } from './components/SidePanel';

// Import services
import { detectGPUUsage, injectGPUMonitoring } from './services/gpu-detection';
import { setupThemeManager, adjustUIForBranding, replaceLogo, setupLogoThemeListener } from './services/theme-manager';
import { updateCreditsDisplay, updateGPUStats } from './services/credits-system';

// Import utilities
import { hashCode } from './utils/helpers';

// Import styles
import '../style/index.css';
import envergeLogoSvg from '../style/enverge.svg';

// WARNING: this must match the name of the extension in the package.json
const placeholderPluginId = 'enverge_placeholder:plugin';

// Add GPU detection functionality to the extension
const extension: JupyterFrontEndPlugin<void> = {
  id: placeholderPluginId,
  autoStart: true,
  requires: [IThemeManager, INotebookTracker],
  optional: [IToolbarWidgetRegistry, ILayoutRestorer],
  activate: async (
    app: JupyterFrontEnd,
    themeManager: IThemeManager,
    notebookTracker: INotebookTracker,
    toolbarRegistry: IToolbarWidgetRegistry,
    restorer: ILayoutRestorer
  ): Promise<void> => {
    console.log('enverge-placeholder extension is activated!');

    // Setup theme management
    const toggleTheme = setupThemeManager(app, themeManager);
    
    // Adjust UI for branding
    adjustUIForBranding();
    
    // Replace logo and pass theme manager
    setTimeout(() => {
      replaceLogo(envergeLogoSvg, themeManager);
      // Set up listener for theme changes
      setupLogoThemeListener(themeManager);
    }, 2000);
    
    // Initialize credits display
    setTimeout(updateCreditsDisplay, 100);

    // Create toggle ID for congestion simulation
    const toggleId = 'cell-alert-toggle';
    
    // Create side panel
    const sidePanel = createSidePanel(toggleId);
    
    // Add to right side panel
    app.shell.add(sidePanel, 'right');
    
    if (restorer) {
      restorer.add(sidePanel, sidePanel.id);
    }

    // Track the update interval
    let updateInterval: number | null = null;
    
    // Track the currently executing cell
    let currentExecutingCellId: string | null = null;
    
    // Unified function to update all GPU-related UI elements and stats
    const updateGPUState = (isGPUActive: boolean): void => {
      // Update the GPU status display
      const gpuStatusElement = document.getElementById('gpu-usage-status');
      if (gpuStatusElement) {
        gpuStatusElement.textContent = isGPUActive ? 'GPU used now' : 'No GPU used';
        gpuStatusElement.style.color = isGPUActive 
          ? 'var(--jp-accent-color1)' 
          : 'var(--jp-ui-font-color1)';
      }
      
      // Update GPU stats (load, memory usage, credits)
      updateGPUStats(isGPUActive);
      
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
          updateGPUStats(stillActive);
          
          // If no longer active, clear the interval
          if (!stillActive && updateInterval !== null) {
            clearInterval(updateInterval);
            updateInterval = null;
          }
        }, 2000);
      } else {
        // Clear the interval when GPU is no longer active
        if (updateInterval !== null) {
          clearInterval(updateInterval);
          updateInterval = null;
        }
      }
    };
    
    if (toolbarRegistry) {
      console.log('Adding widget to toolbar registry', {toolbarRegistry});
      toolbarRegistry.addFactory('TopBar', 'enverge-placeholder', () => {
        console.log('Creating enverge-placeholder widget');
        const widget = ReactWidget.create(
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <ThemeSwitch 
              themeManager={themeManager} 
              onChange={() => toggleTheme()}>
              <span slot="unchecked-message">Light</span>
              <span slot="checked-message">Dark</span>
            </ThemeSwitch>
            <EnergyMixBar />
          </div>
        );
        return widget;
      });
    } else {
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
        NotebookActions.executionScheduled.connect((_, args) => {
          const { cell } = args;
          console.log('Cell execution scheduled, cell ID:', cell.model.id);
          
          // Get the cell's code
          const code = cell.model.sharedModel.getSource();
          
          // Generate a unique ID for this cell based on its content
          const contentHash = hashCode(code);
          const cellId = `${cell.model.id}-${contentHash}`;
          console.log('Generated cell ID for execution:', cellId);
          
          // Check if the code uses GPU
          const usesGPU = detectGPUUsage(code);
          console.log({usesGPU})

          if (usesGPU) {
            console.log('GPU usage detected in cell');
            // Set as current executing cell if it's a GPU cell
            currentExecutingCellId = cellId;
            console.log('Executing GPU cell, current executing cell set to:', currentExecutingCellId);
            
            // Update GPU state to show GPU is active
            updateGPUState(true);
          } else {
            console.log('Executing non-GPU cell');
            
            // Update GPU state to show no GPU usage
            updateGPUState(false);
          }
          
          const toggle = document.getElementById(toggleId) as HTMLInputElement;
          if (toggle?.checked) {
            void showDialog({
              title: 'Congestion Alert',
              body: (
                <div>
                  <CountdownTimer />
                  <div style={{ marginTop: '10px', marginBottom: '10px' }}>
                    <label>
                      Purchase priority runtime (hours):{' '}
                      <select defaultValue="1">
                        <option value="1">1 hour ($3)</option>
                        <option value="4">4 hours ($12)</option>
                        <option value="8">8 hours ($24)</option>
                        <option value="24">24 hours ($150)</option>
                      </select>
                    </label>
                  </div>
                  <button 
                    className="jp-mod-styled"
                    onClick={(e) => {
                      e.preventDefault();
                      const paymentArea = document.getElementById('payment-area');
                      if (paymentArea) {
                        paymentArea.style.display = 'block';
                      }
                    }}
                    style={{
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
                    }}>
                    Purchase Priority Runtime
                  </button>
                  <div 
                    id="payment-area"
                    style={{ 
                      display: 'none',
                      border: '1px solid var(--jp-border-color1)',
                      borderRadius: '4px',
                      padding: '15px',
                      marginTop: '10px'
                    }}>
                    <input
                      type="text"
                      placeholder="Card number"
                      style={{
                        width: '100%',
                        padding: '8px',
                        marginBottom: '10px',
                        border: '1px solid var(--jp-border-color1)',
                        borderRadius: '4px'
                      }}
                    />
                    <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                      <input
                        type="text"
                        placeholder="MM/YY"
                        style={{
                          width: '50%',
                          padding: '8px',
                          border: '1px solid var(--jp-border-color1)',
                          borderRadius: '4px'
                        }}
                      />
                      <input
                        type="text"
                        placeholder="CVC"
                        style={{
                          width: '50%',
                          padding: '8px',
                          border: '1px solid var(--jp-border-color1)',
                          borderRadius: '4px'
                        }}
                      />
                    </div>
                    <button 
                      className="jp-mod-styled"
                      onClick={() => {
                        const cardNumber = (document.querySelector('input[placeholder="Card number"]') as HTMLInputElement)?.value;
                        const expiry = (document.querySelector('input[placeholder="MM/YY"]') as HTMLInputElement)?.value;
                        const cvc = (document.querySelector('input[placeholder="CVC"]') as HTMLInputElement)?.value;
                        
                        alert(`Card Details:\nNumber: ${cardNumber}\nExpiry: ${expiry}\nCVC: ${cvc}`);
                      }}
                      style={{
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
                      }}>
                      Submit Payment
                    </button>
                  </div>
                  <div style={{ marginTop: '10px', textAlign: 'right' }}>
                    <a href="https://docs.enverge.ai" target="_blank" rel="noopener noreferrer">
                      Click here to learn more
                    </a>
                  </div>
                </div>
              ),
              buttons: [
                Dialog.cancelButton()
              ]
            });
          }
        });
        
        // Reset stats after execution completes
        NotebookActions.executed.connect((_, args) => {
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
      injectGPUMonitoring(notebookTracker.currentWidget);
    });
  },
};

export default extension;

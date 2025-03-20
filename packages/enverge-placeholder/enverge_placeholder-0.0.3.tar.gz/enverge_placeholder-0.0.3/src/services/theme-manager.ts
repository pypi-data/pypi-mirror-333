import { JupyterFrontEnd } from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';

export const setupThemeManager = (app: JupyterFrontEnd, themeManager: IThemeManager): () => Promise<void> => {
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
export const adjustUIForBranding = (): void => {
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

    const menuBar = document.getElementsByClassName('lm-MenuBar-content')[0] as HTMLElement;
    menuBar.style.paddingTop = '10px';

    const lmMenuBar = document.getElementsByClassName('lm-MenuBar');
    for (let i = 0; i < lmMenuBar.length; i++) {
      const element = lmMenuBar[i] as HTMLElement;
      element.style.color = 'var(--jp-accent-color1)';
    }
  };
 
  setTimeout(adjustTopPanelHeight, 2000);
};

// Function to replace the Jupyter logo with Enverge logo
export const replaceLogo = (logoSvg: string, themeManager?: IThemeManager): void => {
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
export const updateLogoColors = (svgElement: SVGElement, themeManager?: IThemeManager): void => {
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
export const setupLogoThemeListener = (themeManager: IThemeManager): void => {
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
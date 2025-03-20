import { Widget } from '@lumino/widgets';

export const createSidePanel = (toggleId: string): Widget => {
  const sidePanel = new Widget();
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
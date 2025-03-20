// Credit system state
interface CreditState {
  availableCredits: {
    hours: number;
    minutes: number;
  };
  usageStats: {
    today: number;  // in minutes
    week: number;   // in minutes
    month: number;  // in minutes
  };
}

// Initialize credit state
const creditState: CreditState = {
  availableCredits: {
    hours: 100,
    minutes: 0
  },
  usageStats: {
    today: 270, // 4.5 hours in minutes
    week: 852,  // 14.2 hours in minutes
    month: 2748 // 45.8 hours in minutes
  }
};

// Function to update credits display in the UI
export const updateCreditsDisplay = (): void => {
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
export const decreaseCredits = (): void => {
  if (creditState.availableCredits.minutes > 0) {
    creditState.availableCredits.minutes -= 1;
  } else if (creditState.availableCredits.hours > 0) {
    creditState.availableCredits.hours -= 1;
    creditState.availableCredits.minutes = 59;
  }
  
  // Increase today's usage by 1 minute
  creditState.usageStats.today += 1;
  
  updateCreditsDisplay();
};

// Function to update GPU stats during cell execution
export const updateGPUStats = (gpuUsageDetected: boolean = false): void => {
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
  } else {
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
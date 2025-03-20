import * as React from 'react';
import { useState, useEffect } from 'react';

export const CountdownTimer = () => {
  const [timeLeft, setTimeLeft] = useState({
    hours: 16,
    minutes: 12,
    seconds: 30
  });

  useEffect(() => {
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

  return (
    <>
      <p>
        Our runtime is experiencing high demand. 
      </p>
      <p>
        Your process will execute in{' '}
        <span style={{ fontWeight: 'bold' }}>
          {timeLeft.hours}hours {timeLeft.minutes}minutes and {timeLeft.seconds}seconds
        </span>
      </p>
    </>
  );
}; 
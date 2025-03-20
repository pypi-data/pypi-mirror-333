import { Switch } from '@jupyter/react-components';
import { IThemeManager } from '@jupyterlab/apputils';
import * as React from 'react';
import { useState, useEffect, ChangeEvent } from 'react';

interface IThemeSwitchProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  themeManager: IThemeManager;
  onChange?: (event: ChangeEvent<HTMLInputElement>) => void;
}

export const ThemeSwitch = (props: IThemeSwitchProps) => {
  const { themeManager, onChange, ...others } = props;

  const [dark, setDark] = useState(false);

  const updateChecked = () => {
    const isDark = !themeManager.isLight(themeManager.theme);
    setDark(!!isDark);
  };

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (onChange) {
      onChange(event);
    }
  };

  useEffect(() => {
    let timeout = 0;
    if (!themeManager.theme) {
      // TODO: investigate why the themeManager is undefined
      timeout = setTimeout(() => {
        updateChecked();
      }, 500);
    } else {
      updateChecked();
    }
    themeManager.themeChanged.connect(updateChecked);
    return () => {
      clearTimeout(timeout);
      themeManager.themeChanged.disconnect(updateChecked);
    };
  });

  return <Switch {...others} onChange={handleChange} aria-checked={dark} />;
}; 
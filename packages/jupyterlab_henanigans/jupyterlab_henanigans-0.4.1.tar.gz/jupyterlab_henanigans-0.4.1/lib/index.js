import { IThemeManager } from '@jupyterlab/apputils';
/**
 * Initialization data for the jupyterlab_henanigans extension.
 */
const plugin = {
    id: 'jupyterlab_henanigans:plugin',
    description: 'A dark JupyterLab theme.',
    autoStart: true,
    requires: [IThemeManager],
    activate: (app, manager) => {
        console.log('JupyterLab Henanigans theme is activated!');
        const style = 'jupyterlab_henanigans/index.css';
        manager.register({
            name: 'Henanigans',
            isLight: true,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    }
};
export default plugin;

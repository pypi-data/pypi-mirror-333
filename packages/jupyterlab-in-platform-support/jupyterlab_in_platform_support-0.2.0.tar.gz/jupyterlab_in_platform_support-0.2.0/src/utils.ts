import { ISettingRegistry } from '@jupyterlab/settingregistry';
// import { Dialog, showDialog } from '@jupyterlab/apputils';
// import { INotification } from "jupyterlab_toastify";
// import isEmpty from 'lodash.isempty';

// import { EditSettingsWidget } from "./widgets/EditSettingsWidget"

interface Settings {
    atlasId: string;
    chatlasURL: string;
}

export function loadSettings(setting: ISettingRegistry.ISettings): Settings {
    // Read the settings and convert to the correct type
    let atlasId = setting.get('atlasId-ips').composite as string || "";
    let chatlasURL = setting.get('chatlasURL-ips').composite as string || "";
    return { atlasId, chatlasURL };
}

export async function saveAtlasId(setting: ISettingRegistry.ISettings, atlasId: string): Promise<string> {
    // Read the settings and convert to the correct type
    await setting.set('atlasId-ips', atlasId);
    return atlasId;
}

export async function saveChatlasURL(setting: ISettingRegistry.ISettings, chatlasURL: string): Promise<string> {
    // Read the settings and convert to the correct type
    await setting.set('chatlasURL-ips', chatlasURL);
    return chatlasURL;
}

// export async function configureNewAtlas(settings: ISettingRegistry, pluginId: string): Promise<any> {
//     // Load the current Atlas ID from settings
//     let extensionConfig = await Promise.all([settings.load(pluginId)])
//         .then(([setting]) => {
//             return loadSettings(setting);
//         }).catch((reason) => {
//             INotification.error(`Could not get the configuration. Please contact the administrator.`, { autoClose: 3000 });
//             console.error(
//                 `Something went wrong when getting the current atlas id.\n${reason}`
//             );
//         });

//     // Pass it to the AtlasIdPrompt to show it in the input
//     const newAtlasID = await showDialog({
//         body: new EditSettingsWidget(extensionConfig.atlasId || ""),
//         buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Save" })],
//         focusNodeSelector: "input",
//         title: "Settings"
//     })

//     if (newAtlasID.button.label === "Cancel") {
//         return;
//     }

//     if (isEmpty(newAtlasID.value)) {
//         INotification.error(`Please, insert a valid Atlas Id. Visit help.voiceatlas.com for more information.`, { autoClose: 3000 });
//         return;
//     }

//     // Show notification perhaps using jupyterlab_toastify
//     // Save new atlas id in settings
//     await Promise.all([settings.load(pluginId)])
//         .then(([setting]) => {
//             setting.set('atlasId-ips', newAtlasID.value)
//             INotification.success('Success', {
//                 autoClose: 3000
//             });
//             return newAtlasID.value
//         }).catch((reason) => {
//             INotification.error(`Could not save the configuration. Please contact the administrator.`, {
//                 autoClose: 3000
//             });
//             console.error(
//                 `Something went wrong when setting a new atlas id.\n${reason}`
//             );
//         });
// }
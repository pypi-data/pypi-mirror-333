import { ISettingRegistry } from '@jupyterlab/settingregistry';

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
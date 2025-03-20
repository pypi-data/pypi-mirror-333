import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { PageConfig } from '@jupyterlab/coreutils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { Dialog, MainAreaWidget, showDialog } from '@jupyterlab/apputils';
import { ILauncher } from "@jupyterlab/launcher";
import { Menu, Widget } from '@lumino/widgets';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ChatlasWidget } from './widgets/ChatlasWidget';
import { GetSupportFormWidget } from './widgets/GetSupportFormWidget';
import { aboutVoiceAtlasDialog } from './widgets/AboutWidget';
import { loadSettings } from './utils';
import { getHelpIcon } from './style/IconsStyle';

// import { requestAPI } from './handler';

const PLUGIN_ID = 'jupyterlab-in-platform-support:plugin'
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  description: 'A JupyterLab extension.',
  autoStart: true,
  requires: [IMainMenu, ISettingRegistry, ILauncher],
  activate
};

let atlasId = '';
let chatlasURL = "https://bot.voiceatlas.com/v1/chatlas.js"

/**
 * Initialization data for the jupyterlab-in-platform-support extension.
 */
async function activate(app: JupyterFrontEnd, mainMenu: IMainMenu, settings: ISettingRegistry, launcher: ILauncher): Promise<void> {
  console.log('JupyterLab extension jupyterlab-in-platform-support is activated!');
  const openChatlas = 'jupyterlab-in-platform-support:openChatlas';
  const getSupport = 'jupyterlab-in-platform-support:getSupport';
  const aboutVoiceAtlas = 'jupyterlab-in-platform-support:aboutVoiceAtlas';

  console.log('Loading settings');
  await Promise.all([settings.load(PLUGIN_ID)])
    .then(([setting]) => {
      console.log('Settings loaded');

      let loadedSettings = loadSettings(setting);
      atlasId = loadedSettings.atlasId
      chatlasURL = loadedSettings.chatlasURL
      console.log(`Atlas ID = ${atlasId}`)
      console.log(`Chatlas URL = ${chatlasURL}`)
    }).catch((reason) => {
      console.error(
        `Something went wrong when getting the current atlas id.\n${reason}`
      );
    });

  // Promise.all([app.restored, settings.load(PLUGIN_ID)])
  //   .then(async ([, setting]) => {
  //     let loadedSettings = loadSettings(setting);
  //     atlasId = loadedSettings.atlasId
  //     chatlasURL = loadedSettings.chatlasURL
  //     console.log(`Atlas ID = ${atlasId}`)
  //     console.log(`Chatlas URL = ${chatlasURL}`)
  //   }).catch((reason) => {
  //     console.error(
  //       `Something went wrong when changing the settings.\n${reason}`
  //     );
  //   });

  const menu = new Menu({ commands: app.commands });
  menu.title.label = 'OSS Support'

  app.commands.addCommand(openChatlas, {
    label: 'Support Chat',
    caption: 'Support Chat',
    icon: (args) => (args["isPalette"] ? undefined : getHelpIcon),
    execute: async () => {
      const content = new ChatlasWidget(atlasId, chatlasURL)
      content.title.label = 'Chatlas for JupyterLab';
      const widget = new MainAreaWidget<ChatlasWidget>({ content })
      app.shell.add(widget, 'main');
    }
  });

  app.commands.addCommand(getSupport, {
    label: 'Support Form',
    caption: 'Support Form',
    execute: async () => {
      const currentUser = PageConfig.getOption('serverRoot').split('/')[2] || ""
      const content = new GetSupportFormWidget({ username: currentUser })
      content.title.label = 'Contact Support';
      Widget.attach(content, document.body)
    }
  });

  app.commands.addCommand(aboutVoiceAtlas, {
    label: 'About OSS Support',
    caption: 'About OSS Support',
    execute: async () => {
      const { aboutBody, aboutTitle } = aboutVoiceAtlasDialog();
      const result = await showDialog({
        title: aboutTitle,
        body: aboutBody,
        buttons: [
          Dialog.createButton({
            label: 'Dismiss',
            className: 'jp-About-button jp-mod-reject jp-mod-styled'
          })
        ]
      });

      if (result.button.accept) {
        return;
      }
    }
  })

  menu.addItem({ command: openChatlas });
  menu.addItem({ command: getSupport });
  menu.addItem({ type: 'separator' });
  menu.addItem({ command: aboutVoiceAtlas });

  mainMenu.addMenu(menu, true, { rank: 1000 });

  if (launcher) {
    console.log('There is launcher')
    launcher.add({
      command: openChatlas,
      category: "SMCE Services",
      args: { isLauncher: true }
    });
  } else {
    console.log('There is launcher')
  }
}

export default plugin;

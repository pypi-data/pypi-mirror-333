import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IMainMenu } from '@jupyterlab/mainmenu';
import { MainAreaWidget, ToolbarButton } from '@jupyterlab/apputils';
import { Menu } from '@lumino/widgets';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import isEqual from "lodash.isequal";
import { Dialog, showDialog, Notification } from '@jupyterlab/apputils';
import { DocumentRegistry } from "@jupyterlab/docregistry";
import { NotebookPanel, INotebookModel, INotebookTracker } from "@jupyterlab/notebook";
import { DisposableDelegate, IDisposable } from "@lumino/disposable";

import { ChatlasWidget } from './widgets/ChatlasWidget';
import { loadSetting, configureNewAtlas } from './utils';
import { aboutVoiceAtlasDialog } from './widgets/AboutVoiceAtlas';
import { ChatlasDropdownWidget } from './widgets/ChatlasDropdownMenuWidget';
import EditSettingsWidget from './widgets/EditSettingsWidget';
import isEmpty from 'lodash.isempty';

import { HELP_VA_ENDPOINT, APP_VA_ENDPOINT } from "./globals";

const PLUGIN_ID = 'jupyterlab-va-nb-assistant:plugin'

let globalAtlasId: string | undefined | null = undefined;
let globalNotebookName: string;
let globalApp: JupyterFrontEnd;
let globalPanel: NotebookPanel;


/**
 * Initialization data for the jupyterlab-va-nb-assistant extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  description: 'A JupyterLab extension.',
  autoStart: true,
  requires: [ISettingRegistry, IMainMenu, INotebookTracker],
  activate
};

async function activate(
  app: JupyterFrontEnd,
  settingRegistry: ISettingRegistry,
  mainMenu: IMainMenu,
  notebookTracker: INotebookTracker,
  panel: NotebookPanel): Promise<void> {
  console.log('JupyterLab extension jupyterlab-va-nb-assistant is activated!');

  if (settingRegistry) {
    Promise.all([app.restored, settingRegistry.load(PLUGIN_ID)])
      .then(([, setting]) => {
        loadSetting(setting);
      }).catch((reason) => {
        console.error(
          `Something went wrong when changing the settings.\n${reason}`
        );
      });
  }

  const { commands } = app;
  const openChatlas = 'voice-atlas-jlab-ext:openChatlas';
  const editSettings = 'voice-atlas-jlab-ext:editSettings';
  const createNewAtlas = 'voice-atlas-jlab-ext:createNewAtlas';
  const aboutVoiceAtlas = 'voice-atlas-jlab-ext:aboutVoiceAtlas';
  const helpVoiceAtlas = 'voice-atlas-jlab-ext:helpVoiceAtlas';

  commands.addCommand(openChatlas, {
    label: 'Open Chatlas',
    caption: 'Open Chatlas',
    execute: async () => {
      let atlasId = ''
      await Promise.all([settingRegistry.load(PLUGIN_ID)])
        .then(([setting]) => {
          atlasId = loadSetting(setting);
        }).catch((reason) => {
          console.error(
            `Something went wrong when getting the current atlas id.\n${reason}`
          );
        });

      if (isEqual(atlasId, "")) {
        atlasId = await configureNewAtlas(settingRegistry, PLUGIN_ID)
        return;
      }
      const content = new ChatlasWidget(atlasId, globalNotebookName)
      content.title.label = 'Voice Atlas for JupyterLab';
      const widget = new MainAreaWidget<ChatlasWidget>({ content })
      app.shell.add(widget, 'main');
    }
  });

  commands.addCommand(editSettings, {
    label: 'Edit Settings',
    caption: 'Settings',
    execute: async () => { globalAtlasId ? await configureNewAtlas(settingRegistry, PLUGIN_ID, globalAtlasId) : await configureNewAtlas(settingRegistry, PLUGIN_ID) }
  });

  commands.addCommand(createNewAtlas, {
    label: 'Create new atlas',
    caption: 'Create new atlas.',
    execute: () => {
      const url = APP_VA_ENDPOINT;
      window.open(url);
    }
  });

  commands.addCommand(aboutVoiceAtlas, {
    label: 'About Voice Atlas',
    caption: 'About Voice Atlas',
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

  commands.addCommand(helpVoiceAtlas, {
    label: 'Help',
    caption: 'Help.',
    execute: () => {
      const url = HELP_VA_ENDPOINT;
      window.open(url);
    }
  });

  const menu = new Menu({ commands: app.commands });
  menu.title.label = 'NLP'

  menu.addItem({
    command: createNewAtlas,
    args: { origin: 'from menu' },
  });

  menu.addItem({
    command: editSettings,
    args: { origin: 'from menu' },
  });

  menu.addItem({
    command: openChatlas,
    args: { origin: 'from menu' },
  });

  menu.addItem({ type: 'separator' });

  menu.addItem({
    command: helpVoiceAtlas,
    args: { origin: 'from menu' },
  });

  menu.addItem({
    command: aboutVoiceAtlas,
    args: { origin: 'from menu' },
  });

  mainMenu.addMenu(menu, true, { rank: 1000 });
  app.docRegistry.addWidgetExtension("Notebook", new ButtonExtension());

  notebookTracker.currentChanged.connect(async (_, panel) => {
    if (panel) {
      notebookTracker.currentWidget?.update()
      panel.context.ready.then(async () => {
        let atlasId = panel.model ? panel.model.metadata['atlas-id'] as string : undefined;
        globalAtlasId = atlasId;
        globalNotebookName = panel.title.label.split(".")[0];
        globalPanel = panel;

        if (atlasId) {
          panel.toolbar.insertItem(11, "chatlas", button);
        }
        globalApp = app;
        const chatlasDropdownMenu = new ChatlasDropdownWidget(atlasId)
        panel.toolbar.insertItem(10, "chatlasActions", chatlasDropdownMenu);

        chatlasDropdownMenu.menuOptionChanged.connect(async (_: ChatlasWidget, menuOption: string) => {
          if (isEqual(menuOption, 'set')) {
            const newAtlasID = await showDialog({
              body: new EditSettingsWidget(atlasId || ""),
              buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Save" })],
              focusNodeSelector: "input",
              title: "Settings"
            })

            if (newAtlasID.button.label === "Cancel") {
              return;
            }

            if (isEmpty(newAtlasID.value)) {
              Notification.error(`Please, insert a valid Atlas Id. Visit help.voiceatlas.com for more information.`, { autoClose: 3000 });
              return;
            } else {
              console.log(`Saving Atlas ID => ${newAtlasID.value}`)
              if (panel.model) {
                panel.model.metadata['atlas-id'] = newAtlasID.value;
              }
              app.commands.execute('docmanager:save')
              globalAtlasId = newAtlasID.value;
              panel.toolbar.insertItem(11, "chatlas", button);
            }
          }
          if (isEqual(menuOption, 'delete')) {
            if (panel.model) {
              delete panel.model.metadata['atlas-id'];
            }
            app.commands.execute('docmanager:save')
            panel.toolbar.layout?.removeWidget(button)
            globalAtlasId = undefined
          }
        })
      })
    }
  })
}

const openChatlas = (): void => {
  console.log(`Calling Chatlas => ${globalAtlasId}`)
  const content = new ChatlasWidget(globalAtlasId!, globalNotebookName)
  content.title.label = `Chatlas - ${globalNotebookName}`;
  const widget = new MainAreaWidget<ChatlasWidget>({ content })
  widget.id = `chatlas-${globalNotebookName}`
  console.log(`Current Notebook Panel Info => ${globalPanel.id}`)
  globalApp.shell.add(widget, 'main');
}

let button = new ToolbarButton({
  label: "Chatlas",
  onClick: openChatlas,
  tooltip: "Open Chatlas.",
});

export class ButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  createNew(
    panel: NotebookPanel,
    _: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}

export default plugin;

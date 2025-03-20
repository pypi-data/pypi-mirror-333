import { Widget } from '@lumino/widgets';
import { BOT_VA_ENDPOINT } from "../globals";

export class ChatlasWidget extends Widget {
    constructor(atlasId: string, notebookName: string) {
        super({ node: ChatlasWidget.createChatlasWidget(atlasId, notebookName) })
    }

    private static createChatlasWidget(atlasId: string, notebookName: string): HTMLElement {
        const script = document.createElement('script')
        script.setAttribute("src", BOT_VA_ENDPOINT)
        script.setAttribute("async", "")
        document.body.appendChild(script)

        // Verify if custom element already exists
        // if exists change attribute
        // else define it
        const chatlas = document.createElement('app-chatlas')
        chatlas.setAttribute('name', notebookName)
        chatlas.setAttribute('id', notebookName)
        chatlas.setAttribute("atlas-id", atlasId)
        chatlas.setAttribute("full-screen", "true")
        chatlas.setAttribute("voice-enabled", "true")
        document.body.appendChild(chatlas)
        return chatlas;
    }
}
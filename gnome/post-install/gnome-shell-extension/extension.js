import GObject from 'gi://GObject';
import GLib from 'gi://GLib';
import St from 'gi://St';
import Clutter from 'gi://Clutter';
import Gio from 'gi://Gio';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import { gettext as _ } from 'resource:///org/gnome/shell/extensions/extension.js';

let donationButton;

export default class DonationExtension {
    enable() {
        donationButton = new PanelMenu.Button(0.0, 'DonationButton', false);

        let label = new St.Label({
            text: "Donation",
            y_align: Clutter.ActorAlign.CENTER,
            style_class: 'system-status-icon',
        });

        donationButton.add_child(label);

        donationButton.connect('button-press-event', () => {
            let context = new Gio.AppLaunchContext();

            Gio.AppInfo.launch_default_for_uri(
                'https://www.patreon.com/slackwarelinux',
                context
            );
        });

        Main.panel.addToStatusArea('donationButton', donationButton);
    }

    disable() {
        if (donationButton) {
            donationButton.destroy();
            donationButton = null;
        }
    }
}

/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

import QtGraphicalEffects 1.15
import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Mozilla.VPN 1.0
import "../components"
import "../themes/themes.js" as Theme

VPNFlickable {
    id: vpnFlickable

    flickContentHeight: Theme.settingsMaxContentHeight
    ListModel {
        id: settingsMenuListModel

        ListElement {
            settingTitle: qsTrId("vpn.settings.notifications")
            imageLeftSource: "../resources/settings/notifications.svg"
            imageRightSource: "../resources/chevron.svg"
            pushView: "../settings/ViewNotifications.qml"
        }

        ListElement {
            settingTitle: qsTrId("vpn.settings.networking")
            imageLeftSource: "../resources/settings/networkSettings.svg"
            imageRightSource: "../resources/chevron.svg"
            pushView: "../settings/ViewNetworkSettings.qml"
        }

        ListElement {
            settingTitle: qsTrId("vpn.settings.language")
            imageLeftSource: "../resources/settings/language.svg"
            imageRightSource: "../resources/chevron.svg"
            pushView: "../settings/ViewLanguage.qml"
        }

        ListElement {
            settingTitle: qsTrId("vpn.settings.aboutUs")
            imageLeftSource: "../resources/settings/aboutUs.svg"
            imageRightSource: "../resources/chevron.svg"
            pushView: "../settings/ViewAboutUs.qml"
        }

        ListElement {
            settingTitle: qsTrId("vpn.main.getHelp")
            imageLeftSource: "../resources/settings/getHelp.svg"
            imageRightSource: "../resources/chevron.svg"
            pushGetHelp: true
        }

        ListElement {
            //% "Give feedback"
            settingTitle: qsTrId("vpn.settings.giveFeedback")
            imageLeftSource: "../resources/settings/feedback.svg"
            imageRightSource: "../resources/externalLink.svg"
            openUrl: VPN.LinkFeedback
        }

    }

    VPNIconButton {
        id: iconButton

        onClicked: stackview.pop(StackView.Immediate)
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.topMargin: Theme.windowMargin / 2
        anchors.leftMargin: Theme.windowMargin / 2
        accessibleName: qsTrId("vpn.main.back")

        Image {
            id: backImage

            source: "../resources/close-dark.svg"
            sourceSize.width: Theme.iconSize
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: iconButton
        }

    }

    Image {
        id: logo

        source: VPNUser.avatar
        anchors.horizontalCenter: parent.horizontalCenter
        height: 80
        smooth: true
        fillMode: Image.PreserveAspectFit
        layer.enabled: true
        anchors.top: parent.top
        anchors.topMargin: 32

        Rectangle {
            id: mask

            anchors.fill: parent
            radius: 40
            visible: false
        }

        layer.effect: OpacityMask {
            maskSource: mask
        }

    }

    VPNHeadline {
        id: logoTitle

        //% "VPN User"
        readonly property var textVpnUser: qsTrId("vpn.settings.user")

        text: VPNUser.displayName ? VPNUser.displayName : textVpnUser
        anchors.top: logo.bottom
        anchors.topMargin: Theme.vSpacing
    }

    VPNSubtitle {
        id: logoSubtitle

        text: VPNUser.email
    }

    VPNButton {
        id: manageAccountButton

        //: "Manage account"
        text: qsTrId("vpn.main.manageAccount")
        anchors.top: logoSubtitle.bottom
        anchors.topMargin: Theme.vSpacing
        onClicked: VPN.openLink(VPN.LinkAccount)
    }

    VPNCheckBoxRow {
        id: startAtBootCheckBox

        //: The back of the object, not the front
        //% "Launch VPN app on Startup"
        labelText: qsTrId("vpn.settings.runOnBoot")
        subLabelText: ""
        isChecked: VPNSettings.startAtBoot
        isEnabled: true
        showDivider: true
        anchors.top: manageAccountButton.bottom
        anchors.topMargin: Theme.hSpacing * 1.5
        anchors.rightMargin: Theme.hSpacing
        width: parent.width - Theme.hSpacing
        onClicked: VPNSettings.startAtBoot = !VPNSettings.startAtBoot
    }

    Component {
        id: getHelpComponent

        VPNGetHelp {
            isSettingsView: true
        }

    }

    VPNList {
        id: settingsList

        height: parent.height - manageAccountButton.height - logoSubtitle.height - logoTitle.height - startAtBootCheckBox.height
        width: parent.width
        anchors.top: startAtBootCheckBox.bottom
        anchors.topMargin: Theme.vSpacing
        spacing: Theme.listSpacing
        //% "Settings"
        listName: qsTrId("vpn.main.settings")
        model: settingsMenuListModel

        delegate: VPNClickableRow {
            accessibleName: settingTitle
            onClicked: {
                if (pushGetHelp)
                    return settingsStackView.push(getHelpComponent);

                if (pushView)
                    return settingsStackView.push(pushView);

                return VPN.openLink(openUrl);
            }

            VPNSettingsItem {
                setting: settingTitle
                imageLeftSrc: imageLeftSource
                imageRightSrc: imageRightSource
            }

        }

    }

    VPNSignOut {
        id: signOutLink

        onClicked: VPNController.logout()
    }

}

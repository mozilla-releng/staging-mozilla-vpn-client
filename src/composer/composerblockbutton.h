/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

#ifndef COMPOSERBLOCKBUTTON_H
#define COMPOSERBLOCKBUTTON_H

#include "../addons/addonproperty.h"
#include "composerblock.h"

#include <QJSValue>

class Addon;

class ComposerBlockButton final : public ComposerBlock {
  Q_OBJECT
  Q_DISABLE_COPY_MOVE(ComposerBlockButton)
  QML_NAMED_ELEMENT(VPNComposerBlockButton)
  QML_UNCREATABLE("")

  ADDON_PROPERTY(text, m_text, retranslationCompleted)
  Q_PROPERTY(Style style READ style CONSTANT)

 public:
  enum Style { Primary, Destructive, Link };
  Q_ENUM(Style);

  static ComposerBlock* create(Composer* composer, Addon* addon,
                               const QString& prefix, const QJsonObject& json);
  virtual ~ComposerBlockButton();

  Style style() const { return m_style; }

  Q_INVOKABLE void click() const;

 private:
  ComposerBlockButton(Composer* composer, Style style,
                      const QJSValue& function);

 private:
  AddonProperty m_text;
  const Style m_style;
  const QJSValue m_function;
};

#endif  // COMPOSERBLOCKBUTTON_H
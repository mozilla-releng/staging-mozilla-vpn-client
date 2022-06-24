# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

set -e

# Output directory for task
mkdir -p /builds/worker/artifacts/

# Setup build
sudo yum-builddep -y mozillavpn.spec

# Build RPM
rpmbuild -D "_topdir $(pwd)" -D "_sourcedir $(pwd)" -ba mozillavpn.spec

# Copy artifact (exclude debug rpms)
cp \
 $(find RPMS/ -name '*.rpm' -not -name '*debug*' | head -n 1) \
 /builds/worker/artifacts/mozillavpn.rpm

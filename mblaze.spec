Name:           mblaze
Version:        1.3
Release:        1%{?dist}
Summary:        Unix utilities to deal with Maildir

License:        CC0 and MIT
URL:            https://github.com/leahneukirchen/mblaze
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  sed

Requires: less
Suggests: %{name}-contrib

%package contrib
Summary: Additional utilities for mblaze
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

Requires: /usr/bin/awk
# mopenall
Requires: /usr/bin/xdg-open
# mencrypt, mgpg, msign, mverify
Requires: /usr/bin/gpg2
# mp7m, mverify
Requires: /usr/bin/openssl
# mvi
Requires: /usr/bin/tput
# msearch
Enhances: mairix notmuch maildir-utils
Suggests: mairix notmuch maildir-utils


%description
The mblaze message system is a set of Unix utilities for processing
and interacting with mail messages which are stored in maildir folders.

%description contrib
A few scripts and hacks that are not officially supported or subject to any
robustness, portability or stability criteria.  Use at your own risk.


%prep
%autosetup


%build
%make_build


%install
%make_install PREFIX="/usr"

rm -f _files contrib/_files

make -qp | awk '
    BEGIN { FS = " = " }
    ($1 == "ALL" || $1 == "SCRIPT") {
        split($2, a, " ")
        for (i in a) { print "%{_bindir}/" a[i] }
    }
    $0 ~ "# Implicit Rules" { exit }
' >> _files
ls -1 man | sed -e 's:^:%%{_mandir}/man*/:' -e 's:$:*:' >> _files

pushd contrib
for i in *; do
    case "$i" in
    _*) ;;
    *.md)
        echo "%%doc contrib/$i" >> _files
        ;;
    *.1)
        install -p -D -m0644 "$i" %{?buildroot}%{_mandir}/man1
        echo "%%{_mandir}/man1/${i}*" >> _files
        ;;
    *)
        install -p -D -m0755 "$i" %{?buildroot}%{_bindir}
        echo "%%{_bindir}/$i" >> _files
        ;;
    esac
done
install -D -m0644 -t %{?buildroot}%{_datadir}/zsh/site-functions _mblaze
echo "%%{_datadir}/zsh/site-functions/_mblaze" >> _files
popd


%files -f _files
%license COPYING
%doc README VIOLATIONS.md NEWS.md filter.example mlesskey.example
# These are symlinks generated in `make install`
%{_bindir}/mbnc
%{_bindir}/mfwd
%{_bindir}/mrep
%{_bindir}/mrefile

%files contrib -f contrib/_files
%{nil}  # all in contrib/_files

%changelog
* Thu Apr 03 2025 Thomas Schneider <qsx@chaotikum.eu> 1.3-1
- New upstream release
* Wed Nov 29 2023 Thomas Schneider <qsx@chaotikum.eu> - 1.2-2
- Fix zsh completion install
- Create dependency chain between base and contrib package

* Tue May 10 2022 Thomas Schneider <qsx@chaotikum.eu> - 1.2-1
- Initial packaging

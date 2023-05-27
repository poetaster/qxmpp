Name:           libqxmpp
Version:        1.5.0
Release:        0
Summary:        Qt XMPP Library
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
URL:            https://github.com/qxmpp-project/qxmpp/
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake >= 3.7
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(libomemo-c)
Requires:       pkgconfig(qca)

%description
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package        libs
Summary:        Qt XMPP Library
Group:          System/Libraries
Provides:       libqxmpp-qt5 = %{version}
Obsoletes:      libqxmpp-qt5 < %{version}

%description    libs
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package        devel
Summary:        Qxmpp Development Files
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       pkgconfig(gstreamer-1.0)
Provides:       libqxmpp-qt5-devel = %{version}
Obsoletes:      libqxmpp-qt5-devel < %{version}

%description    devel
Development package for qxmpp.

%package doc
Summary:        Qxmpp library documentation
Group:          Documentation/HTML
BuildArch:      noarch

%description doc
This packages provides documentation of Qxmpp library API.

%prep
%autosetup -n %{name}-%{version}/ron282 -p1

%build
touch .git
mkdir -p build
pushd build

%cmake ../ \
  -DWITH_GSTREAMER=ON \
  -DBUILD_DOCUMENTATION=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_TESTS=OFF \
  -DBUILD_OMEMO=ON \

%make_build
popd

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR=%{buildroot}
popd

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files -n %{name}
%license COPYING
%doc README
%{_libdir}/libQXmppQt5.so*
%{_libdir}/libQXmppOmemoQt5.so*

%files -n %{name}-devel
%{_opt_qt5_includedir}/QXmppQt5/
%{_opt_qt5_libdir}/libQXmppQt5.so*
%{_opt_qt5_libdir}/cmake/QXmppQt5/
%{_opt_qt5_libdir}/cmake/QXmpp/
%{_opt_qt5_libdir}/pkgconfig/QXmppQt5.pc
%{_opt_qt5_libdir}/pkgconfig/qxmpp.pc
%{_opt_qt5_libdir}/libQXmppOmemoQt5.so*
%{_opt_qt5_libdir}/cmake/QXmppOmemoQt5/

%files doc
%{_datadir}/doc/qxmpp/

%changelog


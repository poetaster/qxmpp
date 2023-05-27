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
BuildRequires:  qca-devel
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(libomemo-c)

%description
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package -n     %{name}
Summary:        Qt XMPP Library
Group:          System/Libraries
Provides:       libqxmpp-qt5 = %{version}
Obsoletes:      libqxmpp-qt5 < %{version}

%description -n %{name}%{sover}
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package -n     %{name}-devel
Summary:        Qxmpp Development Files
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       pkgconfig(gstreamer-1.0)
Provides:       libqxmpp-qt5-devel = %{version}
Obsoletes:      libqxmpp-qt5-devel < %{version}

%description -n %{name}-devel
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
%{_libdir}/%{name}.so.*
%{_libdir}/libQXmppOmemo.so.*

%files -n %{name}-devel
%{_includedir}/qxmpp/
%{_libdir}/%{name}.so
%{_libdir}/cmake/qxmpp/
%{_libdir}/pkgconfig/qxmpp.pc
%{_libdir}/libQXmppOmemo.so
%{_libdir}/cmake/QXmppOmemo/

%files doc
%{_datadir}/doc/qxmpp/

%changelog


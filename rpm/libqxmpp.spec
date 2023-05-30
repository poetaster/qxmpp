%global kf5_version 5.106.0

%global __requires_exclude ^libqxmpp.*$|
%global __requires_exclude ^libQXmppOmemo.*$|
%global __requires_exclude ^libqca-qt5.*$|

Name:           opt-kf5-libqxmpp
Version:        1.5
Release:        0
Summary:        Qt XMPP Library
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
URL:            https://github.com/qxmpp-project/qxmpp/
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  cmake >= 3.7
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
#BuildRequires:  doxygen
#BuildRequires:  fdupes

BuildRequires: opt-extra-cmake-modules >= %{kf5_version}
BuildRequires: opt-qt5-qtbase-devel
BuildRequires: opt-qt5-qtdeclarative-devel
BuildRequires: opt-qt5-qttools-devel
BuildRequires: opt-kf5-rpm-macros >= %{kf5_version}
BuildRequires: opt-qt5-qtbase-gui
BuildRequires: opt-qca-qt5-devel
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(libomemo-c)

Requires:      opt-qca-qt5
Requires:      opt-qca-qt5-ossl
Requires:      pkgconfig(libomemo-c)

%{?opt_kf5_default_filter}

%description
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package -n libqxmpp
Summary:	Library for using the XMPP messenging protocol with Qt
Group:		System/Libraries

%description -n libqxmpp
Library for using the XMPP messenging protocol with Qt

%package    devel
Summary:	Development files for QXmpp
Group:		Development/KDE and Qt
Requires:	libqxmpp

%description devel
Development files for QXmpp, a library for using the XMPP messenging
protocol with Qt

%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%_opt_cmake_kf5 ../ \
  -DWITH_GSTREAMER=ON \
  -DBUILD_DOCUMENTATION=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_TESTS=OFF \
  -DWITH_QCA=ON \
  -DBUILD_OMEMO=ON 

%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd

%check
#export LD_LIBRARY_PATH=%{buildroot}%{_libdir}

# Exclude tests needing a network connection
#%{ctest --exclude-regex "tst_(qxmppcallmanager|qxmppiceconnection|qxmppserver|qxmpptransfermanager|qxmppuploadrequestmanager)"}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -n libqxmpp
%license LICENSES/*
%doc AUTHORS CHANGELOG.md README.md
%{_opt_qt5_libdir}/libqxmpp.*
%{_opt_qt5_libdir}/libQXmppOmemo.*

%files  devel
%{_opt_qt5_includedir}/qxmpp/
%{_opt_qt5_libdir}/cmake/qxmpp/
%{_opt_qt5_libdir}/pkgconfig/qxmpp.pc
%{_opt_qt5_libdir}/cmake/QXmppOmemo/
%{_opt_qt5_libdir}/*.so


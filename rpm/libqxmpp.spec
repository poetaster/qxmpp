%global kf5_version 5.106.0
%global qt_version 5.15.9

Name:           opt-kf5-libqxmpp
Version:        1.5
Release:        0
Summary:        Qt XMPP Library
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
URL:            https://github.com/qxmpp-project/qxmpp/
Source0:        %{name}-%{version}.tar.bz2

%{?opt_qt5_default_filter}

BuildRequires:  cmake >= 3.7
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires: opt-extra-cmake-modules >= %{kf5_version}
BuildRequires: opt-qt5-qtbase-devel
BuildRequires: opt-qt5-qtdeclarative-devel
BuildRequires: opt-qt5-qttools-devel
BuildRequires: opt-kf5-rpm-macros >= %{kf5_version}
BuildRequires: opt-qt5-rpm-macros
BuildRequires: opt-qt5-qtbase-gui
BuildRequires: opt-qca-qt5-devel
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(libomemo-c)

Requires:      pkgconfig(libomemo-c)
Requires:      opt-qca-qt5
Requires:      opt-qca-qt5-ossl

%description
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package        devel
Summary:	    Development files for QXmpp
Group:		    Development/KDE and Qt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for QXmpp, a library for using the XMPP messenging
protocol with Qt

%prep
%autosetup -n %{name}-%{version}/ronqxmpp -p1

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
  -DBUILD_OMEMO=ON  \
  -DWITH_OMEMO_V03=ON \

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

%post   devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files -n %{name}                                                     
%license LICENSES/*
%doc AUTHORS CHANGELOG.md README.md
%{_opt_qt5_libdir}/libQXmppQt5.so*                                            
%{_opt_qt5_libdir}/libQXmppOmemoQt5.so*                                       
                                                                      
%files devel                                               
%{_opt_qt5_includedir}/QXmppQt5/                                              
%{_opt_qt5_libdir}/libQXmppQt5.so*                                            
%{_opt_qt5_libdir}/cmake/QXmppQt5/                                            
%{_opt_qt5_libdir}/cmake/QXmpp/                                               
%{_opt_qt5_libdir}/pkgconfig/QXmppQt5.pc                                      
%{_opt_qt5_libdir}/pkgconfig/qxmpp.pc                                         
%{_opt_qt5_libdir}/libQXmppOmemoQt5.so*                                       
%{_opt_qt5_libdir}/cmake/QXmppOmemoQt5/                                       


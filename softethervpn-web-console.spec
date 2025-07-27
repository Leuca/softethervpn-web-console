%global V5_VERSION 5.2.5188
%global V4_VERSION 4.44-9807-rtm

%global ver5 %(echo "%{V5_VERSION}" | cut -d"." -f 1,2)
%global ver4 %(echo "%{V4_VERSION}" | cut -d"-" -f 1)
%global build5 %(echo "%{V5_VERSION}" | cut -d"." -f 3)
%global build4 %(echo "%{V4_VERSION}" | cut -d"-" -f 2)

%global cpu_feature_commit a8397ba4591237c17d18e4acc091f5f3ebe7391e
%global cpu_feature_version 0.6.0

%global major %( echo "%{actual_version}" | cut -d"." -f 1 )

%global console_path src/bin/hamcore/wwwroot/admin/manager
%global ncpu_features s390x 
%global nv4_arches s390x ppc64le 

# Only build console package
%bcond_with console_only

%if %{without console_only}
# For development purposes one might want to skip building the console itself
%bcond_without console

# Optionally skip changing the binary scripts
%bcond_without systemd_aliases

# It is reasonable to pick stable or unstable version and not build both
# Build by default version 5 if the arch is incompatible
%ifarch %{nv4_arches}
%bcond_without v5
%else
%bcond_with v5
%endif

%if %{with v5}
%global actual_version %{ver5}
%global sebuild .build%{build5}
%else
%global actual_version %{ver4}
%global sebuild .build%{build4}
%endif

%else
# If we only build console ensure it is built
%global with_console 1
# The console alone cannot produce debuginfo
%global debug_package %{nil}
%endif
#Console only

%global lead {{{ get_lead }}}
%global follow {{{ get_follow }}}

### Main package aka console
Name:           {{{ git_dir_name }}}
Version:        {{{ git_dir_version lead=%{lead} follow=%{follow} }}}
Release:        8%{?sebuild}%{?dist}

Summary:        A work-in-progress PatternFly 4 web administration console for SoftEtherVPN Software
License:        BSD-3

URL:            https://github.com/Leuca/softethervpn-web-console

# Detailed information about the source Git repository and the source commit
# for the created rpm package
VCS:            {{{ git_dir_vcs }}}

BuildRequires:  npm
BuildRequires:  gettext
BuildRequires:  nodejs
BuildRequires:  wget
BuildRequires:  cmake
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  libsodium-devel
BuildRequires:  readline-devel
BuildRequires:  zlib-devel
BuildRequires:  diffstat
BuildRequires:  doxygen
BuildRequires:  git
BuildRequires:  patch
BuildRequires:  patchutils
BuildRequires:  subversion
BuildRequires:  systemtap
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros

Source0:        {{{ git_dir_pack }}}
Source1:        https://github.com/SoftEtherVPN/SoftEtherVPN/archive/refs/tags/%{V5_VERSION}.tar.gz
Source2:        https://github.com/SoftEtherVPN/SoftEtherVPN_Stable/archive/refs/tags/v%{V4_VERSION}.tar.gz

Patch0:         softethervpn-flags.patch
Patch1:         softethervpn-paths.patch
Patch2:         softethervpn-add-soversion.patch
Patch3:         libcpu_features-shared-lib.patch
Patch4:         softethervpn-fix-implicit-declaration.patch

%description
SoftEtherVPN Patternfly web console aims to allow for easy and complete management of a SoftEtherVPN software instance directly connecting to its built-in web server.
This package only contains the compiled javascript for this project, SoftEtherVPN software binaries are provided in separate packages and do not need this package.

%if %{without console_only}
%package -n softethervpn-common
Summary:        An Open-Source Free Cross-platform Multi-protocol VPN Program
License:        Apache License Version 2.0
URL:            https://github.com/SoftEtherVPN/SoftEtherVPN

%if %{without v5}
ExcludeArch:    %{nv4_arches}
%else
Requires:       softethervpn-libs%{_isa} = %{actual_version}-%{release}
%endif

Version:        %{actual_version}

%description -n softethervpn-common
SoftEther VPN is one of the world's most powerful and easy-to-use multi-protocol VPN software. It runs on Windows, Linux, Mac, FreeBSD, and Solaris.
This package contains common files for software version %{major}

%package -n softethervpn-server
Summary:        An Open-Source Free Cross-platform Multi-protocol VPN Program
License:        Apache License Version 2.0
Requires:       softethervpn-common%{_isa} = %{actual_version}-%{release} 
URL:            https://github.com/SoftEtherVPN/SoftEtherVPN

%if %{without v5}
ExcludeArch:    %{nv4_arches}
%endif

Version:        %{actual_version}

%description -n softethervpn-server
SoftEther VPN ("SoftEther" means "Software Ethernet") is one of the
world's most powerful and easy-to-use multi-protocol VPN software.
This package contains version %{major} server files and binary.

%package -n softethervpn-client
Summary:        An Open-Source Free Cross-platform Multi-protocol VPN Program
License:        Apache License Version 2.0
Requires:       softethervpn-common%{_isa} = %{actual_version}-%{release}
URL:            https://github.com/SoftEtherVPN/SoftEtherVPN

%if %{without v5}
ExcludeArch:    %{nv4_arches}
%endif

Version:        %{actual_version}

%description -n softethervpn-client
SoftEther VPN ("SoftEther" means "Software Ethernet") is one of the
world's most powerful and easy-to-use multi-protocol VPN software.
This package contains version %{major} client files and binary.

%package -n softethervpn-bridge
Summary:        An Open-Source Free Cross-platform Multi-protocol VPN Program
License:        Apache License Version 2.0
Requires:       softethervpn-common%{_isa} = %{actual_version}-%{release}
URL:            https://github.com/SoftEtherVPN/SoftEtherVPN

%if %{without v5}
ExcludeArch:    %{nv4_arches}
%endif

Version:        %{actual_version}

%description -n softethervpn-bridge
SoftEther VPN ("SoftEther" means "Software Ethernet") is one of the
world's most powerful and easy-to-use multi-protocol VPN software.
This package contains version %{major} bridge files and binary.

%if %{with v5}
%package -n softethervpn-libs
Summary:        SoftEtherVPN shared libraries
License:        Apache License Version 2.0
URL:            https://github.com/SoftEtherVPN/SoftEtherVPN

Version:        %{actual_version}

%ifnarch %{ncpu_features}
Requires:       cpu_features%{_isa} = %{cpu_feature_version}-%{release}
%endif

%description -n softethervpn-libs
Package that provides shared libraries needed by SoftEtherVPN software

%package -n softethervpn-devel
Summary:        SoftEtherVPN shared libraries development headers
License:        Apache License Version 2.0
URL:            https://github.com/SoftEtherVPN/SoftEtherVPN

Version:        %{actual_version}

Requires:       softethervpn-libs%{_isa} = %{actual_version}-%{release}

%description -n softethervpn-devel
Development headers of the shared libraries used by SoftEtherVPN

%ifnarch %{ncpu_features}
%package -n cpu_features
Summary:        A cross platform C99 library to get cpu features at runtime.
License:        Apache License Version 2.0
URL:            https://github.com/google/cpu_features

Version:        %{cpu_feature_version}

Provides:       cpu-features

%description -n cpu_features
A cross-platform C library to retrieve CPU features (such as available instructions) at runtime.

%package -n cpu_features-devel
Summary:        Development headers for cpu_features
License:        Apache License Version 2.0
URL:            https://github.com/google/cpu_features

Version:        %{cpu_feature_version}

Provides:       cpu-features-devel

Requires:       cpu_features%{_isa} = %{cpu_feature_version}-%{release}

%description -n cpu_features-devel
Development headers for a cross-platform C library to retrieve CPU features (such as available instructions) at runtime.

%endif

%endif

%endif
#Console only

%prep
%if %{with console_only}
{{{ git_dir_setup_macro }}}
%else
%if %{with v5}
{{{ git_dir_setup_macro }}} -a 1
pushd SoftEtherVPN-%{V5_VERSION}
    %{__patch} -p1 < %PATCH2
    git clone https://github.com/google/cpu_features.git src/Mayaqua/3rdparty/cpu_features
    pushd src/Mayaqua/3rdparty/cpu_features
        git checkout %{cpu_feature_commit}
        %{__patch} -p1 < %PATCH3
    popd
    git clone https://github.com/cxong/tinydir.git 3rdparty/tinydir
    git clone https://github.com/BLAKE2/BLAKE2.git 3rdparty/BLAKE2
    git clone https://github.com/SoftEtherVPN/libhamcore.git src/libhamcore
popd
%else
{{{ git_dir_setup_macro }}} -a 2
pushd SoftEtherVPN_Stable-%{V4_VERSION}
    %{__patch} -p1 < %PATCH0
    %{__patch} -p1 < %PATCH1
    %{__patch} -p1 < %PATCH4
popd
%endif
%endif

%build

%if %{with console}
# Build console
npm install
npm run build
%endif

%if %{without console_only}
# With V5
%if %{with v5}

%if %{with console}
# Put the console in the source tree
mkdir SoftEtherVPN-%{V5_VERSION}/%{console_path}
cp -r dist/* SoftEtherVPN-%{V5_VERSION}/%{console_path}
%endif

pushd SoftEtherVPN-%{V5_VERSION}
    export CMAKE_FLAGS="-DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_SYSTEMD_UNITDIR=%{_unitdir} -DSE_PIDDIR=%{_rundir}/softethervpn -DSE_LOGDIR=%{_localstatedir}/log/softethervpn -DSE_DBDIR=%{_sysconfdir}/softethervpn"
    %configure
    %make_build -C build
popd

# With V4
%else
# Put the console in the source tree
%if %{with console}
mkdir SoftEtherVPN_Stable-%{V4_VERSION}/%{console_path}
cp -r dist/* SoftEtherVPN_Stable-%{V4_VERSION}/%{console_path}
%endif
pushd SoftEtherVPN_Stable-%{V4_VERSION}
    # Allow compiler to create build objects instead of piping
    export CFLAGS=$( echo "%{optflags}" | sed 's/-pipe//' )
    %configure
    %make_build -e
popd

%endif

%endif
#Console only

%install
%if %{without console_only}
# With V5
%if %{with v5}
# Install v5 and generate units
pushd SoftEtherVPN-%{V5_VERSION}
    # Fix sytemd units before installing
    sed -i 's/usr\/libexec\/softether\/vpnserver\/do_not_run/var\/lib\/softethervpn\/vpnserver\/do_not_run/' build/softether-vpnserver.service
    sed -i 's/usr\/libexec\/softether/usr\/libexec\/softethervpn/' build/softether-vpnserver.service
    sed -i 's/Restart=on-failure/Restart=on-failure\nLogsDirectory=softerhervpn\nRuntimeDirectory=softethervpn/' build/softether-vpnserver.service
    sed -i 's/ReadOnlyDirectories=/ReadOnlyPaths=/' build/softether-vpnserver.service
    sed -i 's/ReadWriteDirectories=-\/usr\/libexec\/softether\/vpnserver/ReadWritePaths=-\/etc\/softethervpn\nReadWritePaths=-\/run\/softethervpn\nReadWritePaths=-\/var\/log\/softethervpn/' build/softether-vpnserver.service

    sed -i 's/usr\/libexec\/softether\/vpnbridge\/do_not_run/var\/lib\/softethervpn\/vpnbridge\/do_not_run/' build/softether-vpnbridge.service
    sed -i 's/usr\/libexec\/softether/usr\/libexec\/softethervpn/' build/softether-vpnbridge.service
    sed -i 's/Restart=on-failure/Restart=on-failure\nLogsDirectory=softerhervpn\nRuntimeDirectory=softethervpn/' build/softether-vpnbridge.service
    sed -i 's/ReadOnlyDirectories=/ReadOnlyPaths=/' build/softether-vpnbridge.service
    sed -i 's/ReadWriteDirectories=-\/usr\/libexec\/softether\/vpnserver/ReadWritePaths=-\/etc\/softethervpn\nReadWritePaths=-\/run\/softethervpn\nReadWritePaths=-\/var\/log\/softethervpn/' build/softether-vpnbridge.service

    sed -i 's/usr\/libexec\/softether\/vpnclient\/do_not_run/var\/lib\/softethervpn\/vpnclient\/do_not_run/' build/softether-vpnclient.service
    sed -i 's/usr\/libexec\/softether/usr\/libexec\/softethervpn/' build/softether-vpnclient.service
    sed -i 's/Restart=on-failure/Restart=on-failure\nLogsDirectory=softerhervpn\nRuntimeDirectory=softethervpn/' build/softether-vpnclient.service
    sed -i 's/ReadOnlyDirectories=/ReadOnlyPaths=/' build/softether-vpnclient.service
    sed -i 's/ReadWriteDirectories=-\/usr\/libexec\/softether\/vpnclient/ReadWritePaths=-\/etc\/softethervpn\nReadWritePaths=-\/run\/softethervpn\nReadWritePaths=-\/var\/log\/softethervpn/' build/softether-vpnclient.service

    %make_install -C build    

    # Rename systemd units
    mv %{buildroot}/%{_unitdir}/softether-vpnbridge.service %{buildroot}/%{_unitdir}/softethervpn-bridge.service
    mv %{buildroot}/%{_unitdir}/softether-vpnserver.service %{buildroot}/%{_unitdir}/softethervpn-server.service
    mv %{buildroot}/%{_unitdir}/softether-vpnclient.service %{buildroot}/%{_unitdir}/softethervpn-client.service

    # Rename libexec folders
    mv %{buildroot}%{_libexecdir}/softether %{buildroot}%{_libexecdir}/softethervpn

    # Copy headers
    mkdir -p %{buildroot}%{_includedir}/libcedar
    mkdir -p %{buildroot}%{_includedir}/libmayaqua
    install -m 0644 src/Cedar/*.h %{buildroot}%{_includedir}/libcedar
    install -m 0644 src/Mayaqua/*.h %{buildroot}%{_includedir}/libmayaqua

popd

# With V4
%else

pushd SoftEtherVPN_Stable-%{V4_VERSION}
    mkdir -p %{buildroot}%{_bindir}
    export INSTALL_BINDIR=%{buildroot}%{_bindir}/
    export INSTALL_VPNSERVER_DIR=%{_libexecdir}/softethervpn/vpnserver/
    export INSTALL_VPNBRIDGE_DIR=%{_libexecdir}/softethervpn/vpnbridge/
    export INSTALL_VPNCLIENT_DIR=%{_libexecdir}/softethervpn/vpnclient/
    export INSTALL_VPNCMD_DIR=%{_libexecdir}/softethervpn/vpncmd/
    export INSTALL_BUILDROOT=%{buildroot}
    %make_install -e

    # Fix systemd units to work with this configuration
    sed -i 's/ReadOnlyDirectories=\//ReadOnlyPaths=\//' systemd/softether-vpnserver.service
    sed -i 's/ReadWriteDirectories=-\/opt\/vpnserver/ReadWritePaths=-\/etc\/softethervpn\nReadWritePaths=-\/run\/softethervpn\nReadWritePaths=-\/var\/log\/softethervpn/' systemd/softether-vpnserver.service
    sed -i 's/opt\/vpnserver\/do_not_run/var\/lib\/softethervpn\/do_not_run/' systemd/softether-vpnserver.service
    sed -i 's/opt\/vpnserver/usr\/libexec\/softethervpn\/vpnserver/' systemd/softether-vpnserver.service
    sed -i 's/Restart=on-failure/Restart=on-failure\nLogsDirectory=softerhervpn\nRuntimeDirectory=softethervpn/' systemd/softether-vpnserver.service

    sed -i 's/ReadOnlyDirectories=\//ReadOnlyPaths=\//' systemd/softether-vpnbridge.service
    sed -i 's/ReadWriteDirectories=-\/opt\/vpnbridge/ReadWritePaths=-\/etc\/softethervpn\nReadWritePaths=-\/run\/softethervpn\nReadWritePaths=-\/var\/log\/softethervpn/' systemd/softether-vpnbridge.service
    sed -i 's/opt\/vpnbridge\/do_not_run/var\/lib\/softethervpn\/do_not_run/' systemd/softether-vpnbridge.service
    sed -i 's/opt\/vpnbridge/usr\/libexec\/softethervpn\/vpnbridge/' systemd/softether-vpnbridge.service
    sed -i 's/Restart=on-failure/Restart=on-failure\nLogsDirectory=softerhervpn\nRuntimeDirectory=softethervpn/' systemd/softether-vpnbridge.service

    sed -i 's/ReadOnlyDirectories=\//ReadOnlyPaths=\//' systemd/softether-vpnclient.service
    sed -i 's/ReadWriteDirectories=-\/opt\/vpnclient/ReadWritePaths=-\/etc\/softethervpn\nReadWritePaths=-\/run\/softethervpn\nReadWritePaths=-\/var\/log\/softethervpn/' systemd/softether-vpnclient.service
    sed -i 's/opt\/vpnclient\/do_not_run/var\/lib\/softethervpn\/do_not_run/' systemd/softether-vpnclient.service
    sed -i 's/opt\/vpnclient/usr\/libexec\/softethervpn\/vpnclient/' systemd/softether-vpnclient.service
    sed -i 's/Restart=on-failure/Restart=on-failure\nLogsDirectory=softerhervpn\nRuntimeDirectory=softethervpn/' systemd/softether-vpnclient.service

    %if %{with systemd_aliases}
    # Make the binary scripts use systemctl
    sed -i '2s/.*/\/usr\/bin\/systemctl "$@" softethervpn-server/' %{buildroot}%{_bindir}/vpnserver
    sed -i '2s/.*/\/usr\/bin\/systemctl "$@" softethervpn-bridge/' %{buildroot}%{_bindir}/vpnbridge
    sed -i '2s/.*/\/usr\/bin\/systemctl "$@" softethervpn-client/' %{buildroot}%{_bindir}/vpnclient
    %endif
popd

# Install systemd units
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 SoftEtherVPN_Stable-%{V4_VERSION}/systemd/softether-vpnserver.service %{buildroot}%{_unitdir}/softethervpn-server.service
install -m 0644 SoftEtherVPN_Stable-%{V4_VERSION}/systemd/softether-vpnclient.service %{buildroot}%{_unitdir}/softethervpn-client.service
install -m 0644 SoftEtherVPN_Stable-%{V4_VERSION}/systemd/softether-vpnbridge.service %{buildroot}%{_unitdir}/softethervpn-bridge.service

%endif

# Generate empty folders
mkdir -p %{buildroot}%{_sysconfdir}/softethervpn
mkdir -p %{buildroot}%{_localstatedir}/log/softethervpn
mkdir -p %{buildroot}%{_rundir}/softethervpn
mkdir -p %{buildroot}%{_sharedstatedir}/softethervpn

%endif
#Console only

%if %{with console}
# Install patternfly ui root
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
cp -r dist/* %{buildroot}%{_sharedstatedir}/%{name}/
%endif

%post
%systemd_post softethervpn-server.service
%systemd_post softethervpn-bridge.service
%systemd_post softethervpn-client.service

%preun
%systemd_preun softethervpn-server.service
%systemd_preun softethervpn-bridge.service
%systemd_preun softethervpn-client.service

%postun
%systemd_postun_with_restart softethervpn-server.service
%systemd_postun_with_restart softethervpn-bridge.service
%systemd_postun_with_restart softethervpn-client.service


%files
%if %{with console}
%license LICENSE
%{_sharedstatedir}/%{name}
%endif

%if %{without console_only}
%files -n softethervpn-common
%{_bindir}/vpncmd
%{_sysconfdir}/softethervpn
%{_libexecdir}/softethervpn/vpncmd/vpncmd
%{_libexecdir}/softethervpn/vpncmd/hamcore.se2
%{_localstatedir}/log/softethervpn
%{_sharedstatedir}/softethervpn
%{_rundir}/softethervpn
%if %{with v5}
%license SoftEtherVPN-%{V5_VERSION}/LICENSE

%files -n softethervpn-libs
%{_libdir}/libcedar.so.*
%{_libdir}/libmayaqua.so.*
%license SoftEtherVPN-%{V5_VERSION}/LICENSE

%files -n softethervpn-devel
%{_libdir}/libcedar.so
%{_libdir}/libmayaqua.so
%{_includedir}/libmayaqua/*.h
%{_includedir}/libcedar/*.h
%license SoftEtherVPN-%{V5_VERSION}/LICENSE

# If supported by the arch
%ifnarch %{ncpu_features}
%files -n cpu_features
%license SoftEtherVPN-%{V5_VERSION}/src/Mayaqua/3rdparty/cpu_features/LICENSE
%{_libdir}/libcpu_features.so.*
%{_bindir}/list_cpu_features

%files -n cpu_features-devel
%license SoftEtherVPN-%{V5_VERSION}/src/Mayaqua/3rdparty/cpu_features/LICENSE
%{_libdir}/libcpu_features.so
%{_includedir}/cpu_features/*
%{_libdir}/cmake/CpuFeatures/CpuFeaturesTargets.cmake
%{_libdir}/cmake/CpuFeatures/CpuFeaturesTargets-relwithdebinfo.cmake
#%%{_libdir}/cmake/CpuFeatures/CpuFeaturesTargets-debug.cmake
%{_libdir}/cmake/CpuFeatures/CpuFeaturesConfig.cmake
%{_libdir}/cmake/CpuFeatures/CpuFeaturesConfigVersion.cmake
%endif

%else
%license SoftEtherVPN_Stable-%{V4_VERSION}/LICENSE
%doc SoftEtherVPN_Stable-%{V4_VERSION}/AUTHORS.TXT SoftEtherVPN_Stable-%{V4_VERSION}/ChangeLog SoftEtherVPN_Stable-%{V4_VERSION}/README
%endif

%files -n softethervpn-server
%if %{with v5}
%license SoftEtherVPN-%{V5_VERSION}/LICENSE
%else
%license SoftEtherVPN_Stable-%{V4_VERSION}/LICENSE
%doc SoftEtherVPN_Stable-%{V4_VERSION}/AUTHORS.TXT SoftEtherVPN_Stable-%{V4_VERSION}/ChangeLog SoftEtherVPN_Stable-%{V4_VERSION}/README
%endif
%{_bindir}/vpnserver
%{_libexecdir}/softethervpn/vpnserver/vpnserver
%{_libexecdir}/softethervpn/vpnserver/hamcore.se2
%{_unitdir}/softethervpn-server.service

%files -n softethervpn-bridge
%if %{with v5}
%license SoftEtherVPN-%{V5_VERSION}/LICENSE
%else
%license SoftEtherVPN_Stable-%{V4_VERSION}/LICENSE
%doc SoftEtherVPN_Stable-%{V4_VERSION}/AUTHORS.TXT SoftEtherVPN_Stable-%{V4_VERSION}/ChangeLog SoftEtherVPN_Stable-%{V4_VERSION}/README
%endif
%{_bindir}/vpnbridge
%{_libexecdir}/softethervpn/vpnbridge/vpnbridge
%{_libexecdir}/softethervpn/vpnbridge/hamcore.se2
%{_unitdir}/softethervpn-bridge.service

%files -n softethervpn-client
%if %{with v5}
%license SoftEtherVPN-%{V5_VERSION}/LICENSE
%else
%license SoftEtherVPN_Stable-%{V4_VERSION}/LICENSE
%doc SoftEtherVPN_Stable-%{V4_VERSION}/AUTHORS.TXT SoftEtherVPN_Stable-%{V4_VERSION}/ChangeLog SoftEtherVPN_Stable-%{V4_VERSION}/README
%endif
%{_bindir}/vpnclient
%{_libexecdir}/softethervpn/vpnclient/vpnclient
%{_libexecdir}/softethervpn/vpnclient/hamcore.se2
%{_unitdir}/softethervpn-client.service
%endif
#Console only

%changelog
{{{ git_dir_changelog }}}

%define		core_gitref		6c8cbf0f68e16f71f3d66d9cbc76115af93324ec
%define		crypto_gitref		2217732a29d750400778900d17adf8aa6dd77bda
%define		tfpsacrypto_gitref	76920edddcad00ac41b248e12d937b845df7bedb
%define		mbedtlsframework_gitref	457996474728cb8e968ed21953b72f74d2f536b2
Summary:	CanoKey library for QEMU
Summary(pl.UTF-8):	Biblioteka CanoKey dla QEMU
Name:		canokey-qemu
Version:	1
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/canokeys/canokey-qemu/tags
Source0:	https://github.com/canokeys/canokey-qemu/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7fb9bdb65d568890a18207a6ddfb757d
Source1:	https://github.com/canokeys/canokey-core/archive/%{core_gitref}/canokey-core-%{core_gitref}.tar.gz
# Source1-md5:	a9fd4f1cf856e6acbea59c70eb7f90d6
Source2:	https://github.com/canokeys/canokey-crypto/archive/%{crypto_gitref}/canokey-crypto-%{crypto_gitref}.tar.gz
# Source2-md5:	ac72eed51184d4a3d4e27d7f733a66e1
## private TF-PSA-Crypto is patched for MBEDTLS_ECP_DP_ED25519 support
Source3:	https://github.com/Mbed-TLS/TF-PSA-Crypto/archive/%{tfpsacrypto_gitref}/TF-PSA-Crypto-%{tfpsacrypto_gitref}.tar.gz
# Source3-md5:	494ddf8152ee258a831e23db6c54f672
Source4:	https://github.com/Mbed-TLS/mbedtls-framework/archive/%{mbedtlsframework_gitref}/mbedtls-framework-%{mbedtlsframework_gitref}.tar.gz
# Source4-md5:	66f38441a31249afed5b34b9d6d95021
Patch0:		%{name}-system-libs.patch
URL:		https://github.com/canokeys/canokey-core/
BuildRequires:	cmake >= 3.7
BuildRequires:	gcc >= 6:4.7
BuildRequires:	littlefs-devel >= 2.8
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tinycbor-devel
Requires:	littlefs >= 2.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# library expects symbols provided by qemu
%define		skip_post_check_so	libcanokey-qemu.so.*

%description
This library can be used by QEMU to provide a virtual canokey to the
guest OS.

Note: this is only for testing purpose; there is no warranty on the
security.

%description -l pl.UTF-8
Ta biblioteka może być używana przez QEMU do zapewnienia wirtualnego
klucza canokey dla systemu-gościa.

Uwaga: służy to tylko do celów testowych - nie ma gwarancji
bezpieczeństwa.

%package devel
Summary:	Header files for canokey-qemu library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki canokey-qemu
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for canokey-qemu library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki canokey-qemu.

%prep
%setup -q

%{__tar} xf %{SOURCE1} -C canokey-core --strip-components=1
%{__tar} xf %{SOURCE2} -C canokey-core/canokey-crypto --strip-components=1
%{__tar} xf %{SOURCE3} -C canokey-core/canokey-crypto/tf-psa-crypto --strip-components=1
%{__tar} xf %{SOURCE4} -C canokey-core/canokey-crypto/tf-psa-crypto/framework --strip-components=1

%patch -P0 -p1

%{__sed} -i -e 's,git describe --always --tags --long --abbrev=8 --dirty,echo %{core_gitref},' canokey-core/CMakeLists.txt

%build
install -d build
cd build
# set BUILD_SHARED_LIBS to OFF to link libcanokey-core statically into libcanokey-qemu
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libcanokey-qemu.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcanokey-qemu.so
%{_includedir}/canokey-qemu.h
%{_pkgconfigdir}/canokey-qemu.pc

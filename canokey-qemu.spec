%define		core_gitref	e216aa00b95b27c8e6bc5f2907a05e49a0ddafad
%define		crypto_gitref	8fab8813ce2603ba198a9beeb32c06ad08ae0865
%define		mbedtls_gitref	f71e2878084126737cc39083e1e15afc459bd93d
Summary:	CanoKey library for QEMU
Summary(pl.UTF-8):	Biblioteka CanoKey dla QEMU
Name:		canokey-qemu
Version:	0
%define	gitref	151568c34f5e92b086b7a3a62a11c43dd39f628b
%define	snap	20230606
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/canokeys/canokey-qemu/tags
Source0:	https://github.com/canokeys/canokey-qemu/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	02b14bbbdbe0e0774f3b8bdb3e201a40
Source1:	https://github.com/canokeys/canokey-core/archive/%{core_gitref}/canokey-core-%{core_gitref}.tar.gz
# Source1-md5:	68d90de51a4279965e172dc58f3beb5f
Source2:	https://github.com/canokeys/canokey-crypto/archive/%{crypto_gitref}/canokey-crypto-%{crypto_gitref}.tar.gz
# Source2-md5:	2f0b6d9c6ededec1fb57f04c2c5b0b7e
## private mbedtls is patched for MBEDTLS_ECP_DP_ED25519 support
Source3:	https://github.com/ARMmbed/mbedtls/archive/%{mbedtls_gitref}/mbedtls-%{mbedtls_gitref}.tar.gz
# Source3-md5:	80fe94ab2e3eb4213d00ba0473dbe71c
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
%setup -q -n %{name}-%{gitref}

%{__tar} xf %{SOURCE1} -C canokey-core --strip-components=1
%{__tar} xf %{SOURCE2} -C canokey-core/canokey-crypto --strip-components=1
%{__tar} xf %{SOURCE3} -C canokey-core/canokey-crypto/mbedtls --strip-components=1

%patch0 -p1

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
%attr(755,root,root) %{_libdir}/libcanokey-qemu.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcanokey-qemu.so
%{_includedir}/canokey-qemu.h
%{_pkgconfigdir}/canokey-qemu.pc

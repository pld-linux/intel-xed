Summary:	Intel X86 Encoder Decoder (Intel XED)
Summary(pl.UTF-8):	Dekoder/koder rozkazów procesorów Intel X86 (Intel XED)
Name:		intel-xed
Version:	12.0.1
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/intelxed/xed/tags
Source0:	https://github.com/intelxed/xed/archive/%{version}/xed-%{version}.tar.gz
# Source0-md5:	4726cdf5f0ddf3320e1dc6f7a80a1758
%define	mbuild_gitref	09b6654be0c52bf1df44e88c88b411a67b624cbd
%define	mbuild_snap	20210417
Source1:	https://github.com/intelxed/mbuild/archive/%{mbuild_gitref}/mbuild-%{mbuild_snap}.tar.gz
# Source1-md5:	f884ed9920720afc7aa57d9474786ef4
Patch0:		xed-default-abi.patch
URL:		https://github.com/intelxed/xed
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-distro
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Intel X86 Encoder Decoder (Intel XED).

%description -l pl.UTF-8
Dekoder/koder rozkazów procesorów Intel X86 (Intel XED).

%package devel
Summary:	Header files for Intel XED libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Intel XED
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Intel XED libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Intel XED.

%prep
%setup -q -n xed-%{version} -a1
%{__mv} mbuild-%{mbuild_gitref} mbuild
%patch0 -p1

%build
PYTHONPATH=$(pwd)/mbuild \
%{__python3} mfile.py install \
	CC="%{__cc}" \
	LINK="%{__cc}" \
	--extra-ccflags="%{rpmcflags} %{rpmcppflags}" \
	--extra-linkflags="%{rpmldflags}" \
	--shared \
	--verbose 6

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

kit=$(echo kits/xed-install-base-*)
install $kit/lib/lib*.so $RPM_BUILD_ROOT%{_libdir}
cp -pr $kit/include/xed $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libxed.so
%attr(755,root,root) %{_libdir}/libxed-ild.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/xed

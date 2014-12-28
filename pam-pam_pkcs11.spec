Summary:	PAM login module that allows a X.509 certificate based user login
Summary(pl.UTF-8):	Moduł PAM umożliwiający logowanie się w oparciu o certyfikat X.509
Name:		pam-pam_pkcs11
Version:	0.6.8
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.opensc-project.org/files/pam_pkcs11/pam_pkcs11-%{version}.tar.gz
# Source0-md5:	5ca42826b60ffcb574cc16b965f56b00
URL:		http://www.opensc-project.org/pam_pkcs11/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	libxslt-progs
BuildRequires:	libtool
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pcsc-lite-devel >= 1.6.0
BuildRequires:	pkgconfig
Requires:	pcsc-lite-libs >= 1.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/%{_lib}

%description
This PAM login module allows a X.509 certificate based user login. The
certificate and its dedicated private key are thereby accessed by
means of an appropriate PKCS#11 module. For the verification of the
users' certificates, locally stored CA certificates as well as either
online or locally accessible CRLs are used.

%description -l pl.UTF-8
Ten moduł PAM umożliwia logowanie się w oparciu o certyfikaty X.509.
Certyfikat i jego klucz prywatny są odczytywane poprzez odpowiedni
moduł PKCS#11. Do weryfikacji certyfikatów użytkowników używane są
lokalnie przechowywane certyfikaty CA albo dostępne lokalnie lub
zdalnie CRL.

%prep
%setup -q -n pam_pkcs11-%{version}

%{__rm} po/stamp-po

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I aclocal
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-curl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_pkcs11.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pam_pkcs11/*.la

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{pt_br,pt_BR}

%find_lang pam_pkcs11

%clean
rm -rf $RPM_BUILD_ROOT

%files -f pam_pkcs11.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/{README.*,*.html,*.css} etc/*.example
%attr(755,root,root) %{_bindir}/card_eventmgr
%attr(755,root,root) %{_bindir}/pkcs11_*
%attr(755,root,root) %{_bindir}/pklogin_finder
%attr(755,root,root) /%{_lib}/security/pam_pkcs11.so
%dir %{_libdir}/pam_pkcs11
%attr(755,root,root) %{_libdir}/pam_pkcs11/*.so
%{_mandir}/man1/card_eventmgr.1*
%{_mandir}/man1/pkcs11_*.1*
%{_mandir}/man1/pklogin_finder.1*
%{_mandir}/man8/pam_pkcs11.8*

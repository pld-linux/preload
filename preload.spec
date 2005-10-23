Summary:	Adaptive readahead daemon
Summary(pl):	Adaptacyjny demon czytania z wyprzedzeniem
Name:		preload
Version:	0.2
Release:	0.4
License:	GPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/preload/%{name}-%{version}.tar.gz
# Source0-md5:	8df1c86c43b8976dc6ee5d45e8ac901c
Source1:	%{name}.init
Patch0:		%{name}-build.patch
URL:		http://preload.sourceforge.net/
BuildRequires:	autoconf >= 2.56
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
preload is an adaptive readahead daemon. It monitors applications that
users run, and by analyzing this data, predicts what applications
users might run, and fetches those binaries and their dependencies
into memory for faster startup times.

%description -l pl
preload to adaptacyny demon czytania z wyprzedzeniem. Monitoruje
aplikacje uruchamiane przez u¿ytkowników i, poprzez analizê tych
danych, przewiduje które aplikacje u¿ytkownicy mog± uruchamiaæ, a
nastêpnie pobiera te binaria i ich zale¿no¶ci do pamiêci w celu
szybszego ich uruchamiania.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/preload

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog TODO THANKS NEWS doc/*.txt
%attr(755,root,root) %{_sbindir}/preload
%config %{_sysconfdir}/preload.conf
%{_mandir}/man8/preload.8*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/preload
%attr(754,root,root) /etc/rc.d/init.d/preload
%attr(644,root,root) /etc/logrotate.d/preload
%attr(600,root,root) %verify(not md5 mtime size) %config(missingok,noreplace) %{_localstatedir}/log/preload.log
%attr(660,root,root) %verify(not md5 mtime size) %ghost %config(missingok,noreplace) %{_localstatedir}/lib/misc/preload.state

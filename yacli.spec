%define section         free
%define gcj_support     1

Name:           yacli
Version:        0.2.3
Release:        0.0.6
Epoch:          0
Summary:        org.freecompany.util
License:        MIT
Group:          Development/Java
URL:            http://www.freecompany.org/
# svn export https://svn.freecompany.org/public/util/tags/yacli-0.2.3
# zip -9r yacli-src-0.2.3.zip yacli-0.2.3
Source0:        http://repository.freecompany.org/org/freecompany/yacli/zips/yacli-src-%{version}.zip
Source1:        yacli-0.2.3-build.xml
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  junit
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif

%description
org.freecompany.util

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__cp} -a %{SOURCE1} build.xml
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
export CLASSPATH=$(build-classpath junit)
export OPT_JAR_LIST="ant/ant-junit"
%{ant} jar javadoc test

%install
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Wed Sep 09 2009 Thierry Vignaud <tvignaud@mandriva.com> 0:0.2.3-0.0.4mdv2010.0
+ Revision: 435329
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:0.2.3-0.0.3mdv2009.0
+ Revision: 136631
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:0.2.3-0.0.3mdv2008.1
+ Revision: 121065
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:0.2.3-0.0.2mdv2008.0
+ Revision: 87325
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Tue Aug 07 2007 David Walluck <walluck@mandriva.org> 0:0.2.3-0.0.1mdv2008.0
+ Revision: 59603
- Import yacli


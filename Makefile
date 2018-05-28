all:
	mcs test.cs -r:System.Data -r:System.Drawing -r:System.DirectoryServices -r:System.Web.Services -r:System.Windows.Forms -r:System.Web.Caching
	mono test.exe
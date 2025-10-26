# Changelog

## [Unreleased]

### Fixed
- Dashboard no longer hangs indefinitely on loading spinner when server/DB is unresponsive
- Added timeouts (8s) to all API calls to prevent UI from hanging
- Added visible error banner with retry button in dashboard when API calls fail
- Added better error handling in auth, loan, and transaction API calls

### Changed
- All frontend fetch calls now use apiCall helper with timeout handling
- Server-side MongoDB connections now timeout quickly (5s) instead of hanging
- Disabled Flask reloader in development to avoid Windows socket issues
- Updated Python dependencies to pinned versions

### Dependencies
- Flask==2.3.3
- Flask-PyMongo==2.3.0
- Flask-CORS==4.0.0
- bcrypt==4.0.1
- pymongo==4.5.0
- dnspython==2.4.2
- Werkzeug==2.3.7

### Development
- Added dashboard error handling and timeout fixes
- Added MongoDB connectivity check at startup
- Removed duplicate JavaScript declarations in dashboard template
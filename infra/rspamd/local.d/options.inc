# Basic Rspamd options
dns {
  timeout = 1s;
  retransmits = 2;
}

# Minimal logging for development
logging {
  type = "console";
  level = "info";
}

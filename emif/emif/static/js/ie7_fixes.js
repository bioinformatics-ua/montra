// no console command on ie 7
if (typeof console == "undefined") {
    this.console = {log: function() {}};
}

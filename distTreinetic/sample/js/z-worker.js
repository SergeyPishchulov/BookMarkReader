! function(t) {
    "use strict";

    function e(t) {
        t.scripts && t.scripts.length > 0 && importScripts.apply(void 0, t.scripts), postMessage({
            type: "importScripts"
        })
    }

    function r(e) {
        var r = t[e.codecClass],
            c = e.sn;
        if (i[c]) throw Error("duplicated sn");
        i[c] = {
            codec: new r(e.options),
            crcInput: "input" === e.crcType,
            crcOutput: "output" === e.crcType,
            crc: new o
        }, postMessage({
            type: "newTask",
            sn: c
        })
    }

    function c(t) {
        var e = t.sn,
            c = t.type,
            n = t.data,
            s = i[e];
        !s && t.codecClass && (r(t), s = i[e]);
        var o, p = "append" === c,
            a = u();
        if (p) try {
            o = s.codec.append(n, function(t) {
                postMessage({
                    type: "progress",
                    sn: e,
                    loaded: t
                })
            })
        } catch (t) {
            throw delete i[e], t
        } else delete i[e], o = s.codec.flush();
        var f = u() - a;
        a = u(), n && s.crcInput && s.crc.append(n), o && s.crcOutput && s.crc.append(o);
        var d = u() - a,
            h = {
                type: c,
                sn: e,
                codecTime: f,
                crcTime: d
            },
            l = [];
        o && (h.data = o, l.push(o.buffer)), p || !s.crcInput && !s.crcOutput || (h.crc = s.crc.get());
        try {
            postMessage(h, l)
        } catch (t) {
            postMessage(h)
        }
    }

    function n(t, e, r) {
        var c = {
            type: t,
            sn: e,
            error: s(r)
        };
        postMessage(c)
    }

    function s(t) {
        return {
            message: t.message,
            stack: t.stack
        }
    }

    function o() {
        this.crc = -1
    }

    function p() {}
    if (t.zWorkerInitialized) throw new Error("z-worker.js should be run only once");
    t.zWorkerInitialized = !0, addEventListener("message", function(t) {
        var e = t.data,
            r = e.type,
            c = e.sn,
            s = a[r];
        if (s) try {
            s(e)
        } catch (t) {
            n(r, c, t)
        }
    });
    var a = {
            importScripts: e,
            newTask: r,
            append: c,
            flush: c
        },
        i = {},
        u = t.performance ? t.performance.now.bind(t.performance) : Date.now;
    o.prototype.append = function(t) {
        for (var e = 0 | this.crc, r = this.table, c = 0, n = 0 | t.length; c < n; c++) e = e >>> 8 ^ r[255 & (e ^ t[c])];
        this.crc = e
    }, o.prototype.get = function() {
        return ~this.crc
    }, o.prototype.table = function() {
        var t, e, r, c = [];
        for (t = 0; t < 256; t++) {
            for (r = t, e = 0; e < 8; e++) 1 & r ? r = r >>> 1 ^ 3988292384 : r >>>= 1;
            c[t] = r
        }
        return c
    }(), t.NOOP = p, p.prototype.append = function(t, e) {
        return t
    }, p.prototype.flush = function() {}
}(this);
//# sourceMappingURL=z-worker.js.map
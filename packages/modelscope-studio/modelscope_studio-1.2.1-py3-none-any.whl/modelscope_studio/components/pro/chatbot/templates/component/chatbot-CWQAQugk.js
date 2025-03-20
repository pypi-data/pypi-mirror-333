var Mn = (e) => {
  throw TypeError(e);
};
var Ln = (e, t, n) => t.has(e) || Mn("Cannot " + n);
var ze = (e, t, n) => (Ln(e, t, "read from private field"), n ? n.call(e) : t.get(e)), Nn = (e, t, n) => t.has(e) ? Mn("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, n), Fn = (e, t, n, r) => (Ln(e, t, "write to private field"), r ? r.call(e, n) : t.set(e, n), n);
import { i as Io, a as ve, r as Mo, b as Lo, w as dt, g as No, c as k, d as wn, e as mt, o as jn } from "./Index-ktPRG3K4.js";
const M = window.ms_globals.React, c = window.ms_globals.React, To = window.ms_globals.React.isValidElement, Q = window.ms_globals.React.useRef, $o = window.ms_globals.React.useLayoutEffect, we = window.ms_globals.React.useEffect, Po = window.ms_globals.React.useCallback, ge = window.ms_globals.React.useMemo, Ro = window.ms_globals.React.forwardRef, Qe = window.ms_globals.React.useState, On = window.ms_globals.ReactDOM, ht = window.ms_globals.ReactDOM.createPortal, Fo = window.ms_globals.antdIcons.FileTextFilled, Oo = window.ms_globals.antdIcons.CloseCircleFilled, jo = window.ms_globals.antdIcons.FileExcelFilled, ko = window.ms_globals.antdIcons.FileImageFilled, Ao = window.ms_globals.antdIcons.FileMarkdownFilled, zo = window.ms_globals.antdIcons.FilePdfFilled, Do = window.ms_globals.antdIcons.FilePptFilled, Ho = window.ms_globals.antdIcons.FileWordFilled, Bo = window.ms_globals.antdIcons.FileZipFilled, Vo = window.ms_globals.antdIcons.PlusOutlined, Wo = window.ms_globals.antdIcons.LeftOutlined, Xo = window.ms_globals.antdIcons.RightOutlined, Uo = window.ms_globals.antdIcons.CloseOutlined, Rr = window.ms_globals.antdIcons.CheckOutlined, Go = window.ms_globals.antdIcons.DeleteOutlined, Ko = window.ms_globals.antdIcons.EditOutlined, qo = window.ms_globals.antdIcons.SyncOutlined, Yo = window.ms_globals.antdIcons.DislikeOutlined, Qo = window.ms_globals.antdIcons.LikeOutlined, Zo = window.ms_globals.antdIcons.CopyOutlined, Jo = window.ms_globals.antdIcons.ArrowDownOutlined, ei = window.ms_globals.antd.ConfigProvider, Ir = window.ms_globals.antd.Upload, yt = window.ms_globals.antd.theme, ti = window.ms_globals.antd.Progress, ie = window.ms_globals.antd.Button, _e = window.ms_globals.antd.Flex, Te = window.ms_globals.antd.Typography, ni = window.ms_globals.antd.Avatar, ri = window.ms_globals.antd.Popconfirm, oi = window.ms_globals.antd.Tooltip, ii = window.ms_globals.antd.Collapse, si = window.ms_globals.antd.Input, Mr = window.ms_globals.createItemsContext.createItemsContext, ai = window.ms_globals.internalContext.useContextPropsContext, kn = window.ms_globals.internalContext.ContextPropsProvider, Ve = window.ms_globals.antdCssinjs.unit, Wt = window.ms_globals.antdCssinjs.token2CSSVar, An = window.ms_globals.antdCssinjs.useStyleRegister, li = window.ms_globals.antdCssinjs.useCSSVarRegister, ci = window.ms_globals.antdCssinjs.createTheme, ui = window.ms_globals.antdCssinjs.useCacheToken, Lr = window.ms_globals.antdCssinjs.Keyframes, vt = window.ms_globals.components.Markdown;
var fi = /\s/;
function di(e) {
  for (var t = e.length; t-- && fi.test(e.charAt(t)); )
    ;
  return t;
}
var mi = /^\s+/;
function pi(e) {
  return e && e.slice(0, di(e) + 1).replace(mi, "");
}
var zn = NaN, gi = /^[-+]0x[0-9a-f]+$/i, hi = /^0b[01]+$/i, yi = /^0o[0-7]+$/i, vi = parseInt;
function Dn(e) {
  if (typeof e == "number")
    return e;
  if (Io(e))
    return zn;
  if (ve(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = ve(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = pi(e);
  var n = hi.test(e);
  return n || yi.test(e) ? vi(e.slice(2), n ? 2 : 8) : gi.test(e) ? zn : +e;
}
var Xt = function() {
  return Mo.Date.now();
}, bi = "Expected a function", Si = Math.max, xi = Math.min;
function wi(e, t, n) {
  var r, o, i, s, a, l, u = 0, f = !1, m = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(bi);
  t = Dn(t) || 0, ve(n) && (f = !!n.leading, m = "maxWait" in n, i = m ? Si(Dn(n.maxWait) || 0, t) : i, d = "trailing" in n ? !!n.trailing : d);
  function h(v) {
    var x = r, P = o;
    return r = o = void 0, u = v, s = e.apply(P, x), s;
  }
  function y(v) {
    return u = v, a = setTimeout(b, t), f ? h(v) : s;
  }
  function g(v) {
    var x = v - l, P = v - u, N = t - x;
    return m ? xi(N, i - P) : N;
  }
  function p(v) {
    var x = v - l, P = v - u;
    return l === void 0 || x >= t || x < 0 || m && P >= i;
  }
  function b() {
    var v = Xt();
    if (p(v))
      return w(v);
    a = setTimeout(b, g(v));
  }
  function w(v) {
    return a = void 0, d && r ? h(v) : (r = o = void 0, s);
  }
  function E() {
    a !== void 0 && clearTimeout(a), u = 0, r = l = o = a = void 0;
  }
  function _() {
    return a === void 0 ? s : w(Xt());
  }
  function C() {
    var v = Xt(), x = p(v);
    if (r = arguments, o = this, l = v, x) {
      if (a === void 0)
        return y(l);
      if (m)
        return clearTimeout(a), a = setTimeout(b, t), h(l);
    }
    return a === void 0 && (a = setTimeout(b, t)), s;
  }
  return C.cancel = E, C.flush = _, C;
}
function _i(e, t) {
  return Lo(e, t);
}
var Nr = {
  exports: {}
}, _t = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ci = c, Ei = Symbol.for("react.element"), Ti = Symbol.for("react.fragment"), $i = Object.prototype.hasOwnProperty, Pi = Ci.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ri = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Fr(e, t, n) {
  var r, o = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) $i.call(t, r) && !Ri.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: Ei,
    type: e,
    key: i,
    ref: s,
    props: o,
    _owner: Pi.current
  };
}
_t.Fragment = Ti;
_t.jsx = Fr;
_t.jsxs = Fr;
Nr.exports = _t;
var S = Nr.exports;
const {
  SvelteComponent: Ii,
  assign: Hn,
  binding_callbacks: Bn,
  check_outros: Mi,
  children: Or,
  claim_element: jr,
  claim_space: Li,
  component_subscribe: Vn,
  compute_slots: Ni,
  create_slot: Fi,
  detach: De,
  element: kr,
  empty: Wn,
  exclude_internal_props: Xn,
  get_all_dirty_from_scope: Oi,
  get_slot_changes: ji,
  group_outros: ki,
  init: Ai,
  insert_hydration: pt,
  safe_not_equal: zi,
  set_custom_element_data: Ar,
  space: Di,
  transition_in: gt,
  transition_out: rn,
  update_slot_base: Hi
} = window.__gradio__svelte__internal, {
  beforeUpdate: Bi,
  getContext: Vi,
  onDestroy: Wi,
  setContext: Xi
} = window.__gradio__svelte__internal;
function Un(e) {
  let t, n;
  const r = (
    /*#slots*/
    e[7].default
  ), o = Fi(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = kr("svelte-slot"), o && o.c(), this.h();
    },
    l(i) {
      t = jr(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Or(t);
      o && o.l(s), s.forEach(De), this.h();
    },
    h() {
      Ar(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      pt(i, t, s), o && o.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && Hi(
        o,
        r,
        i,
        /*$$scope*/
        i[6],
        n ? ji(
          r,
          /*$$scope*/
          i[6],
          s,
          null
        ) : Oi(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (gt(o, i), n = !0);
    },
    o(i) {
      rn(o, i), n = !1;
    },
    d(i) {
      i && De(t), o && o.d(i), e[9](null);
    }
  };
}
function Ui(e) {
  let t, n, r, o, i = (
    /*$$slots*/
    e[4].default && Un(e)
  );
  return {
    c() {
      t = kr("react-portal-target"), n = Di(), i && i.c(), r = Wn(), this.h();
    },
    l(s) {
      t = jr(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Or(t).forEach(De), n = Li(s), i && i.l(s), r = Wn(), this.h();
    },
    h() {
      Ar(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      pt(s, t, a), e[8](t), pt(s, n, a), i && i.m(s, a), pt(s, r, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && gt(i, 1)) : (i = Un(s), i.c(), gt(i, 1), i.m(r.parentNode, r)) : i && (ki(), rn(i, 1, 1, () => {
        i = null;
      }), Mi());
    },
    i(s) {
      o || (gt(i), o = !0);
    },
    o(s) {
      rn(i), o = !1;
    },
    d(s) {
      s && (De(t), De(n), De(r)), e[8](null), i && i.d(s);
    }
  };
}
function Gn(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Gi(e, t, n) {
  let r, o, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = Ni(i);
  let {
    svelteInit: l
  } = t;
  const u = dt(Gn(t)), f = dt();
  Vn(e, f, (_) => n(0, r = _));
  const m = dt();
  Vn(e, m, (_) => n(1, o = _));
  const d = [], h = Vi("$$ms-gr-react-wrapper"), {
    slotKey: y,
    slotIndex: g,
    subSlotIndex: p
  } = No() || {}, b = l({
    parent: h,
    props: u,
    target: f,
    slot: m,
    slotKey: y,
    slotIndex: g,
    subSlotIndex: p,
    onDestroy(_) {
      d.push(_);
    }
  });
  Xi("$$ms-gr-react-wrapper", b), Bi(() => {
    u.set(Gn(t));
  }), Wi(() => {
    d.forEach((_) => _());
  });
  function w(_) {
    Bn[_ ? "unshift" : "push"](() => {
      r = _, f.set(r);
    });
  }
  function E(_) {
    Bn[_ ? "unshift" : "push"](() => {
      o = _, m.set(o);
    });
  }
  return e.$$set = (_) => {
    n(17, t = Hn(Hn({}, t), Xn(_))), "svelteInit" in _ && n(5, l = _.svelteInit), "$$scope" in _ && n(6, s = _.$$scope);
  }, t = Xn(t), [r, o, f, m, a, l, s, i, w, E];
}
class Ki extends Ii {
  constructor(t) {
    super(), Ai(this, t, Gi, Ui, zi, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: ql
} = window.__gradio__svelte__internal, Kn = window.ms_globals.rerender, Ut = window.ms_globals.tree;
function qi(e, t = {}) {
  function n(r) {
    const o = dt(), i = new Ki({
      ...r,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, l = s.parent ?? Ut;
          return l.nodes = [...l.nodes, a], Kn({
            createPortal: ht,
            node: Ut
          }), s.onDestroy(() => {
            l.nodes = l.nodes.filter((u) => u.svelteInstance !== o), Kn({
              createPortal: ht,
              node: Ut
            });
          }), a;
        },
        ...r.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const Yi = "1.0.5", Qi = /* @__PURE__ */ c.createContext({}), Zi = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Ct = (e) => {
  const t = c.useContext(Qi);
  return c.useMemo(() => ({
    ...Zi,
    ...t[e]
  }), [t[e]]);
};
function Ce() {
  return Ce = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n) ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, Ce.apply(null, arguments);
}
function $e() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r,
    theme: o
  } = c.useContext(ei.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r
  };
}
function Pe(e) {
  var t = M.useRef();
  t.current = e;
  var n = M.useCallback(function() {
    for (var r, o = arguments.length, i = new Array(o), s = 0; s < o; s++)
      i[s] = arguments[s];
    return (r = t.current) === null || r === void 0 ? void 0 : r.call.apply(r, [t].concat(i));
  }, []);
  return n;
}
function Ji(e) {
  if (Array.isArray(e)) return e;
}
function es(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var r, o, i, s, a = [], l = !0, u = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (r = i.call(n)).done) && (a.push(r.value), a.length !== t); l = !0) ;
    } catch (f) {
      u = !0, o = f;
    } finally {
      try {
        if (!l && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function qn(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, r = Array(t); n < t; n++) r[n] = e[n];
  return r;
}
function ts(e, t) {
  if (e) {
    if (typeof e == "string") return qn(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? qn(e, t) : void 0;
  }
}
function ns() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function te(e, t) {
  return Ji(e) || es(e, t) || ts(e, t) || ns();
}
function Et() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var Yn = Et() ? M.useLayoutEffect : M.useEffect, zr = function(t, n) {
  var r = M.useRef(!0);
  Yn(function() {
    return t(r.current);
  }, n), Yn(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, Qn = function(t, n) {
  zr(function(r) {
    if (!r)
      return t();
  }, n);
};
function Ze(e) {
  var t = M.useRef(!1), n = M.useState(e), r = te(n, 2), o = r[0], i = r[1];
  M.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, l) {
    l && t.current || i(a);
  }
  return [o, s];
}
function Gt(e) {
  return e !== void 0;
}
function rs(e, t) {
  var n = t || {}, r = n.defaultValue, o = n.value, i = n.onChange, s = n.postState, a = Ze(function() {
    return Gt(o) ? o : Gt(r) ? typeof r == "function" ? r() : r : typeof e == "function" ? e() : e;
  }), l = te(a, 2), u = l[0], f = l[1], m = o !== void 0 ? o : u, d = s ? s(m) : m, h = Pe(i), y = Ze([m]), g = te(y, 2), p = g[0], b = g[1];
  Qn(function() {
    var E = p[0];
    u !== E && h(u, E);
  }, [p]), Qn(function() {
    Gt(o) || f(o);
  }, [o]);
  var w = Pe(function(E, _) {
    f(E, _), b([m], _);
  });
  return [d, w];
}
function Z(e) {
  "@babel/helpers - typeof";
  return Z = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Z(e);
}
var Dr = {
  exports: {}
}, D = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var _n = Symbol.for("react.element"), Cn = Symbol.for("react.portal"), Tt = Symbol.for("react.fragment"), $t = Symbol.for("react.strict_mode"), Pt = Symbol.for("react.profiler"), Rt = Symbol.for("react.provider"), It = Symbol.for("react.context"), os = Symbol.for("react.server_context"), Mt = Symbol.for("react.forward_ref"), Lt = Symbol.for("react.suspense"), Nt = Symbol.for("react.suspense_list"), Ft = Symbol.for("react.memo"), Ot = Symbol.for("react.lazy"), is = Symbol.for("react.offscreen"), Hr;
Hr = Symbol.for("react.module.reference");
function ce(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case _n:
        switch (e = e.type, e) {
          case Tt:
          case Pt:
          case $t:
          case Lt:
          case Nt:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case os:
              case It:
              case Mt:
              case Ot:
              case Ft:
              case Rt:
                return e;
              default:
                return t;
            }
        }
      case Cn:
        return t;
    }
  }
}
D.ContextConsumer = It;
D.ContextProvider = Rt;
D.Element = _n;
D.ForwardRef = Mt;
D.Fragment = Tt;
D.Lazy = Ot;
D.Memo = Ft;
D.Portal = Cn;
D.Profiler = Pt;
D.StrictMode = $t;
D.Suspense = Lt;
D.SuspenseList = Nt;
D.isAsyncMode = function() {
  return !1;
};
D.isConcurrentMode = function() {
  return !1;
};
D.isContextConsumer = function(e) {
  return ce(e) === It;
};
D.isContextProvider = function(e) {
  return ce(e) === Rt;
};
D.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === _n;
};
D.isForwardRef = function(e) {
  return ce(e) === Mt;
};
D.isFragment = function(e) {
  return ce(e) === Tt;
};
D.isLazy = function(e) {
  return ce(e) === Ot;
};
D.isMemo = function(e) {
  return ce(e) === Ft;
};
D.isPortal = function(e) {
  return ce(e) === Cn;
};
D.isProfiler = function(e) {
  return ce(e) === Pt;
};
D.isStrictMode = function(e) {
  return ce(e) === $t;
};
D.isSuspense = function(e) {
  return ce(e) === Lt;
};
D.isSuspenseList = function(e) {
  return ce(e) === Nt;
};
D.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Tt || e === Pt || e === $t || e === Lt || e === Nt || e === is || typeof e == "object" && e !== null && (e.$$typeof === Ot || e.$$typeof === Ft || e.$$typeof === Rt || e.$$typeof === It || e.$$typeof === Mt || e.$$typeof === Hr || e.getModuleId !== void 0);
};
D.typeOf = ce;
Dr.exports = D;
var Kt = Dr.exports, ss = Symbol.for("react.element"), as = Symbol.for("react.transitional.element"), ls = Symbol.for("react.fragment");
function cs(e) {
  return (
    // Base object type
    e && Z(e) === "object" && // React Element type
    (e.$$typeof === ss || e.$$typeof === as) && // React Fragment type
    e.type === ls
  );
}
var us = function(t, n) {
  typeof t == "function" ? t(n) : Z(t) === "object" && t && "current" in t && (t.current = n);
}, fs = function(t) {
  var n, r;
  if (!t)
    return !1;
  if (Br(t) && t.props.propertyIsEnumerable("ref"))
    return !0;
  var o = Kt.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((n = o.prototype) !== null && n !== void 0 && n.render) && o.$$typeof !== Kt.ForwardRef || typeof t == "function" && !((r = t.prototype) !== null && r !== void 0 && r.render) && t.$$typeof !== Kt.ForwardRef);
};
function Br(e) {
  return /* @__PURE__ */ To(e) && !cs(e);
}
var ds = function(t) {
  if (t && Br(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function ms(e, t) {
  if (Z(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var r = n.call(e, t);
    if (Z(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Vr(e) {
  var t = ms(e, "string");
  return Z(t) == "symbol" ? t : t + "";
}
function V(e, t, n) {
  return (t = Vr(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function Zn(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(e);
    t && (r = r.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), n.push.apply(n, r);
  }
  return n;
}
function j(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? Zn(Object(n), !0).forEach(function(r) {
      V(e, r, n[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : Zn(Object(n)).forEach(function(r) {
      Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(n, r));
    });
  }
  return e;
}
const nt = /* @__PURE__ */ c.createContext(null);
function Jn(e) {
  const {
    getDropContainer: t,
    className: n,
    prefixCls: r,
    children: o
  } = e, {
    disabled: i
  } = c.useContext(nt), [s, a] = c.useState(), [l, u] = c.useState(null);
  if (c.useEffect(() => {
    const d = t == null ? void 0 : t();
    s !== d && a(d);
  }, [t]), c.useEffect(() => {
    if (s) {
      const d = () => {
        u(!0);
      }, h = (p) => {
        p.preventDefault();
      }, y = (p) => {
        p.relatedTarget || u(!1);
      }, g = (p) => {
        u(!1), p.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", h), document.addEventListener("dragleave", y), document.addEventListener("drop", g), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", h), document.removeEventListener("dragleave", y), document.removeEventListener("drop", g);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const m = `${r}-drop-area`;
  return /* @__PURE__ */ ht(/* @__PURE__ */ c.createElement("div", {
    className: k(m, n, {
      [`${m}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: l ? "block" : "none"
    }
  }, o), s);
}
function er(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function ps(e) {
  return e && Z(e) === "object" && er(e.nativeElement) ? e.nativeElement : er(e) ? e : null;
}
function gs(e) {
  var t = ps(e);
  if (t)
    return t;
  if (e instanceof c.Component) {
    var n;
    return (n = On.findDOMNode) === null || n === void 0 ? void 0 : n.call(On, e);
  }
  return null;
}
function hs(e, t) {
  if (e == null) return {};
  var n = {};
  for (var r in e) if ({}.hasOwnProperty.call(e, r)) {
    if (t.includes(r)) continue;
    n[r] = e[r];
  }
  return n;
}
function tr(e, t) {
  if (e == null) return {};
  var n, r, o = hs(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (r = 0; r < i.length; r++) n = i[r], t.includes(n) || {}.propertyIsEnumerable.call(e, n) && (o[n] = e[n]);
  }
  return o;
}
var ys = /* @__PURE__ */ M.createContext({});
function Ue(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function nr(e, t) {
  for (var n = 0; n < t.length; n++) {
    var r = t[n];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, Vr(r.key), r);
  }
}
function Ge(e, t, n) {
  return t && nr(e.prototype, t), n && nr(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function on(e, t) {
  return on = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, on(e, t);
}
function jt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && on(e, t);
}
function bt(e) {
  return bt = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, bt(e);
}
function Wr() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Wr = function() {
    return !!e;
  })();
}
function Ie(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function vs(e, t) {
  if (t && (Z(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Ie(e);
}
function kt(e) {
  var t = Wr();
  return function() {
    var n, r = bt(e);
    if (t) {
      var o = bt(this).constructor;
      n = Reflect.construct(r, arguments, o);
    } else n = r.apply(this, arguments);
    return vs(this, n);
  };
}
var bs = /* @__PURE__ */ function(e) {
  jt(n, e);
  var t = kt(n);
  function n() {
    return Ue(this, n), t.apply(this, arguments);
  }
  return Ge(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(M.Component);
function Ss(e) {
  var t = M.useReducer(function(a) {
    return a + 1;
  }, 0), n = te(t, 2), r = n[1], o = M.useRef(e), i = Pe(function() {
    return o.current;
  }), s = Pe(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, r();
  });
  return [i, s];
}
var Ee = "none", it = "appear", st = "enter", at = "leave", rr = "none", de = "prepare", He = "start", Be = "active", En = "end", Xr = "prepared";
function or(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function xs(e, t) {
  var n = {
    animationend: or("Animation", "AnimationEnd"),
    transitionend: or("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var ws = xs(Et(), typeof window < "u" ? window : {}), Ur = {};
if (Et()) {
  var _s = document.createElement("div");
  Ur = _s.style;
}
var lt = {};
function Gr(e) {
  if (lt[e])
    return lt[e];
  var t = ws[e];
  if (t)
    for (var n = Object.keys(t), r = n.length, o = 0; o < r; o += 1) {
      var i = n[o];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Ur)
        return lt[e] = t[i], lt[e];
    }
  return "";
}
var Kr = Gr("animationend"), qr = Gr("transitionend"), Yr = !!(Kr && qr), ir = Kr || "animationend", sr = qr || "transitionend";
function ar(e, t) {
  if (!e) return null;
  if (Z(e) === "object") {
    var n = t.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const Cs = function(e) {
  var t = Q();
  function n(o) {
    o && (o.removeEventListener(sr, e), o.removeEventListener(ir, e));
  }
  function r(o) {
    t.current && t.current !== o && n(t.current), o && o !== t.current && (o.addEventListener(sr, e), o.addEventListener(ir, e), t.current = o);
  }
  return M.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [r, n];
};
var Qr = Et() ? $o : we, Zr = function(t) {
  return +setTimeout(t, 16);
}, Jr = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Zr = function(t) {
  return window.requestAnimationFrame(t);
}, Jr = function(t) {
  return window.cancelAnimationFrame(t);
});
var lr = 0, Tn = /* @__PURE__ */ new Map();
function eo(e) {
  Tn.delete(e);
}
var sn = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  lr += 1;
  var r = lr;
  function o(i) {
    if (i === 0)
      eo(r), t();
    else {
      var s = Zr(function() {
        o(i - 1);
      });
      Tn.set(r, s);
    }
  }
  return o(n), r;
};
sn.cancel = function(e) {
  var t = Tn.get(e);
  return eo(e), Jr(t);
};
const Es = function() {
  var e = M.useRef(null);
  function t() {
    sn.cancel(e.current);
  }
  function n(r) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = sn(function() {
      o <= 1 ? r({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : n(r, o - 1);
    });
    e.current = i;
  }
  return M.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var Ts = [de, He, Be, En], $s = [de, Xr], to = !1, Ps = !0;
function no(e) {
  return e === Be || e === En;
}
const Rs = function(e, t, n) {
  var r = Ze(rr), o = te(r, 2), i = o[0], s = o[1], a = Es(), l = te(a, 2), u = l[0], f = l[1];
  function m() {
    s(de, !0);
  }
  var d = t ? $s : Ts;
  return Qr(function() {
    if (i !== rr && i !== En) {
      var h = d.indexOf(i), y = d[h + 1], g = n(i);
      g === to ? s(y, !0) : y && u(function(p) {
        function b() {
          p.isCanceled() || s(y, !0);
        }
        g === !0 ? b() : Promise.resolve(g).then(b);
      });
    }
  }, [e, i]), M.useEffect(function() {
    return function() {
      f();
    };
  }, []), [m, i];
};
function Is(e, t, n, r) {
  var o = r.motionEnter, i = o === void 0 ? !0 : o, s = r.motionAppear, a = s === void 0 ? !0 : s, l = r.motionLeave, u = l === void 0 ? !0 : l, f = r.motionDeadline, m = r.motionLeaveImmediately, d = r.onAppearPrepare, h = r.onEnterPrepare, y = r.onLeavePrepare, g = r.onAppearStart, p = r.onEnterStart, b = r.onLeaveStart, w = r.onAppearActive, E = r.onEnterActive, _ = r.onLeaveActive, C = r.onAppearEnd, v = r.onEnterEnd, x = r.onLeaveEnd, P = r.onVisibleChanged, N = Ze(), O = te(N, 2), I = O[0], T = O[1], A = Ss(Ee), L = te(A, 2), R = L[0], F = L[1], W = Ze(null), X = te(W, 2), Y = X[0], B = X[1], z = R(), K = Q(!1), J = Q(null);
  function U() {
    return n();
  }
  var oe = Q(!1);
  function Ne() {
    F(Ee), B(null, !0);
  }
  var ue = Pe(function(re) {
    var ee = R();
    if (ee !== Ee) {
      var pe = U();
      if (!(re && !re.deadline && re.target !== pe)) {
        var rt = oe.current, ot;
        ee === it && rt ? ot = C == null ? void 0 : C(pe, re) : ee === st && rt ? ot = v == null ? void 0 : v(pe, re) : ee === at && rt && (ot = x == null ? void 0 : x(pe, re)), rt && ot !== !1 && Ne();
      }
    }
  }), qe = Cs(ue), Fe = te(qe, 1), Oe = Fe[0], je = function(ee) {
    switch (ee) {
      case it:
        return V(V(V({}, de, d), He, g), Be, w);
      case st:
        return V(V(V({}, de, h), He, p), Be, E);
      case at:
        return V(V(V({}, de, y), He, b), Be, _);
      default:
        return {};
    }
  }, be = M.useMemo(function() {
    return je(z);
  }, [z]), ke = Rs(z, !e, function(re) {
    if (re === de) {
      var ee = be[de];
      return ee ? ee(U()) : to;
    }
    if (H in be) {
      var pe;
      B(((pe = be[H]) === null || pe === void 0 ? void 0 : pe.call(be, U(), null)) || null);
    }
    return H === Be && z !== Ee && (Oe(U()), f > 0 && (clearTimeout(J.current), J.current = setTimeout(function() {
      ue({
        deadline: !0
      });
    }, f))), H === Xr && Ne(), Ps;
  }), $ = te(ke, 2), G = $[0], H = $[1], Se = no(H);
  oe.current = Se;
  var fe = Q(null);
  Qr(function() {
    if (!(K.current && fe.current === t)) {
      T(t);
      var re = K.current;
      K.current = !0;
      var ee;
      !re && t && a && (ee = it), re && t && i && (ee = st), (re && !t && u || !re && m && !t && u) && (ee = at);
      var pe = je(ee);
      ee && (e || pe[de]) ? (F(ee), G()) : F(Ee), fe.current = t;
    }
  }, [t]), we(function() {
    // Cancel appear
    (z === it && !a || // Cancel enter
    z === st && !i || // Cancel leave
    z === at && !u) && F(Ee);
  }, [a, i, u]), we(function() {
    return function() {
      K.current = !1, clearTimeout(J.current);
    };
  }, []);
  var Ae = M.useRef(!1);
  we(function() {
    I && (Ae.current = !0), I !== void 0 && z === Ee && ((Ae.current || I) && (P == null || P(I)), Ae.current = !0);
  }, [I, z]);
  var Vt = Y;
  return be[de] && H === He && (Vt = j({
    transition: "none"
  }, Vt)), [z, H, Vt, I ?? t];
}
function Ms(e) {
  var t = e;
  Z(e) === "object" && (t = e.transitionSupport);
  function n(o, i) {
    return !!(o.motionName && t && i !== !1);
  }
  var r = /* @__PURE__ */ M.forwardRef(function(o, i) {
    var s = o.visible, a = s === void 0 ? !0 : s, l = o.removeOnLeave, u = l === void 0 ? !0 : l, f = o.forceRender, m = o.children, d = o.motionName, h = o.leavedClassName, y = o.eventProps, g = M.useContext(ys), p = g.motion, b = n(o, p), w = Q(), E = Q();
    function _() {
      try {
        return w.current instanceof HTMLElement ? w.current : gs(E.current);
      } catch {
        return null;
      }
    }
    var C = Is(b, a, _, o), v = te(C, 4), x = v[0], P = v[1], N = v[2], O = v[3], I = M.useRef(O);
    O && (I.current = !0);
    var T = M.useCallback(function(X) {
      w.current = X, us(i, X);
    }, [i]), A, L = j(j({}, y), {}, {
      visible: a
    });
    if (!m)
      A = null;
    else if (x === Ee)
      O ? A = m(j({}, L), T) : !u && I.current && h ? A = m(j(j({}, L), {}, {
        className: h
      }), T) : f || !u && !h ? A = m(j(j({}, L), {}, {
        style: {
          display: "none"
        }
      }), T) : A = null;
    else {
      var R;
      P === de ? R = "prepare" : no(P) ? R = "active" : P === He && (R = "start");
      var F = ar(d, "".concat(x, "-").concat(R));
      A = m(j(j({}, L), {}, {
        className: k(ar(d, x), V(V({}, F, F && R), d, typeof d == "string")),
        style: N
      }), T);
    }
    if (/* @__PURE__ */ M.isValidElement(A) && fs(A)) {
      var W = ds(A);
      W || (A = /* @__PURE__ */ M.cloneElement(A, {
        ref: T
      }));
    }
    return /* @__PURE__ */ M.createElement(bs, {
      ref: E
    }, A);
  });
  return r.displayName = "CSSMotion", r;
}
const Ls = Ms(Yr);
var an = "add", ln = "keep", cn = "remove", qt = "removed";
function Ns(e) {
  var t;
  return e && Z(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, j(j({}, t), {}, {
    key: String(t.key)
  });
}
function un() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(Ns);
}
function Fs() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], r = 0, o = t.length, i = un(e), s = un(t);
  i.forEach(function(u) {
    for (var f = !1, m = r; m < o; m += 1) {
      var d = s[m];
      if (d.key === u.key) {
        r < m && (n = n.concat(s.slice(r, m).map(function(h) {
          return j(j({}, h), {}, {
            status: an
          });
        })), r = m), n.push(j(j({}, d), {}, {
          status: ln
        })), r += 1, f = !0;
        break;
      }
    }
    f || n.push(j(j({}, u), {}, {
      status: cn
    }));
  }), r < o && (n = n.concat(s.slice(r).map(function(u) {
    return j(j({}, u), {}, {
      status: an
    });
  })));
  var a = {};
  n.forEach(function(u) {
    var f = u.key;
    a[f] = (a[f] || 0) + 1;
  });
  var l = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return l.forEach(function(u) {
    n = n.filter(function(f) {
      var m = f.key, d = f.status;
      return m !== u || d !== cn;
    }), n.forEach(function(f) {
      f.key === u && (f.status = ln);
    });
  }), n;
}
var Os = ["component", "children", "onVisibleChanged", "onAllRemoved"], js = ["status"], ks = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function As(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Ls, n = /* @__PURE__ */ function(r) {
    jt(i, r);
    var o = kt(i);
    function i() {
      var s;
      Ue(this, i);
      for (var a = arguments.length, l = new Array(a), u = 0; u < a; u++)
        l[u] = arguments[u];
      return s = o.call.apply(o, [this].concat(l)), V(Ie(s), "state", {
        keyEntities: []
      }), V(Ie(s), "removeKey", function(f) {
        s.setState(function(m) {
          var d = m.keyEntities.map(function(h) {
            return h.key !== f ? h : j(j({}, h), {}, {
              status: qt
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var m = s.state.keyEntities, d = m.filter(function(h) {
            var y = h.status;
            return y !== qt;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Ge(i, [{
      key: "render",
      value: function() {
        var a = this, l = this.state.keyEntities, u = this.props, f = u.component, m = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var h = tr(u, Os), y = f || M.Fragment, g = {};
        return ks.forEach(function(p) {
          g[p] = h[p], delete h[p];
        }), delete h.keys, /* @__PURE__ */ M.createElement(y, h, l.map(function(p, b) {
          var w = p.status, E = tr(p, js), _ = w === an || w === ln;
          return /* @__PURE__ */ M.createElement(t, Ce({}, g, {
            key: E.key,
            visible: _,
            eventProps: E,
            onVisibleChanged: function(v) {
              d == null || d(v, {
                key: E.key
              }), v || a.removeKey(E.key);
            }
          }), function(C, v) {
            return m(j(j({}, C), {}, {
              index: b
            }), v);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, l) {
        var u = a.keys, f = l.keyEntities, m = un(u), d = Fs(f, m);
        return {
          keyEntities: d.filter(function(h) {
            var y = f.find(function(g) {
              var p = g.key;
              return h.key === p;
            });
            return !(y && y.status === qt && h.status === cn);
          })
        };
      }
    }]), i;
  }(M.Component);
  return V(n, "defaultProps", {
    component: "div"
  }), n;
}
const zs = As(Yr);
function Ds(e, t) {
  const {
    children: n,
    upload: r,
    rootClassName: o
  } = e, i = c.useRef(null);
  return c.useImperativeHandle(t, () => i.current), /* @__PURE__ */ c.createElement(Ir, Ce({}, r, {
    showUploadList: !1,
    rootClassName: o,
    ref: i
  }), n);
}
const ro = /* @__PURE__ */ c.forwardRef(Ds);
var oo = /* @__PURE__ */ Ge(function e() {
  Ue(this, e);
}), io = "CALC_UNIT", Hs = new RegExp(io, "g");
function Yt(e) {
  return typeof e == "number" ? "".concat(e).concat(io) : e;
}
var Bs = /* @__PURE__ */ function(e) {
  jt(n, e);
  var t = kt(n);
  function n(r, o) {
    var i;
    Ue(this, n), i = t.call(this), V(Ie(i), "result", ""), V(Ie(i), "unitlessCssVar", void 0), V(Ie(i), "lowPriority", void 0);
    var s = Z(r);
    return i.unitlessCssVar = o, r instanceof n ? i.result = "(".concat(r.result, ")") : s === "number" ? i.result = Yt(r) : s === "string" && (i.result = r), i;
  }
  return Ge(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(Yt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(Yt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var i = this, s = o || {}, a = s.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(u) {
        return i.result.includes(u);
      }) && (l = !1), this.result = this.result.replace(Hs, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(oo), Vs = /* @__PURE__ */ function(e) {
  jt(n, e);
  var t = kt(n);
  function n(r) {
    var o;
    return Ue(this, n), o = t.call(this), V(Ie(o), "result", 0), r instanceof n ? o.result = r.result : typeof r == "number" && (o.result = r), o;
  }
  return Ge(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof n ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof n ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(oo), Ws = function(t, n) {
  var r = t === "css" ? Bs : Vs;
  return function(o) {
    return new r(o, n);
  };
}, cr = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function ur(e, t, n, r) {
  var o = j({}, t[e]);
  if (r != null && r.deprecatedTokens) {
    var i = r.deprecatedTokens;
    i.forEach(function(a) {
      var l = te(a, 2), u = l[0], f = l[1];
      if (o != null && o[u] || o != null && o[f]) {
        var m;
        (m = o[f]) !== null && m !== void 0 || (o[f] = o == null ? void 0 : o[u]);
      }
    });
  }
  var s = j(j({}, n), o);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var so = typeof CSSINJS_STATISTIC < "u", fn = !0;
function Ke() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!so)
    return Object.assign.apply(Object, [{}].concat(t));
  fn = !1;
  var r = {};
  return t.forEach(function(o) {
    if (Z(o) === "object") {
      var i = Object.keys(o);
      i.forEach(function(s) {
        Object.defineProperty(r, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[s];
          }
        });
      });
    }
  }), fn = !0, r;
}
var fr = {};
function Xs() {
}
var Us = function(t) {
  var n, r = t, o = Xs;
  return so && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), r = new Proxy(t, {
    get: function(s, a) {
      if (fn) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return s[a];
    }
  }), o = function(s, a) {
    var l;
    fr[s] = {
      global: Array.from(n),
      component: j(j({}, (l = fr[s]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: r,
    keys: n,
    flush: o
  };
};
function dr(e, t, n) {
  if (typeof n == "function") {
    var r;
    return n(Ke(t, (r = t[e]) !== null && r !== void 0 ? r : {}));
  }
  return n ?? {};
}
function Gs(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "max(".concat(r.map(function(i) {
        return Ve(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "min(".concat(r.map(function(i) {
        return Ve(i);
      }).join(","), ")");
    }
  };
}
var Ks = 1e3 * 60 * 10, qs = /* @__PURE__ */ function() {
  function e() {
    Ue(this, e), V(this, "map", /* @__PURE__ */ new Map()), V(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), V(this, "nextID", 0), V(this, "lastAccessBeat", /* @__PURE__ */ new Map()), V(this, "accessBeat", 0);
  }
  return Ge(e, [{
    key: "set",
    value: function(n, r) {
      this.clear();
      var o = this.getCompositeKey(n);
      this.map.set(o, r), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var r = this.getCompositeKey(n), o = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var r = this, o = n.map(function(i) {
        return i && Z(i) === "object" ? "obj_".concat(r.getObjectID(i)) : "".concat(Z(i), "_").concat(i);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var r = this.nextID;
      return this.objectIDMap.set(n, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(o, i) {
          r - o > Ks && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), mr = new qs();
function Ys(e, t) {
  return c.useMemo(function() {
    var n = mr.get(t);
    if (n)
      return n;
    var r = e();
    return mr.set(t, r), r;
  }, t);
}
var Qs = function() {
  return {};
};
function Zs(e) {
  var t = e.useCSP, n = t === void 0 ? Qs : t, r = e.useToken, o = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, h, y, g) {
    var p = Array.isArray(d) ? d[0] : d;
    function b(P) {
      return "".concat(String(p)).concat(P.slice(0, 1).toUpperCase()).concat(P.slice(1));
    }
    var w = (g == null ? void 0 : g.unitless) || {}, E = typeof a == "function" ? a(d) : {}, _ = j(j({}, E), {}, V({}, b("zIndexPopup"), !0));
    Object.keys(w).forEach(function(P) {
      _[b(P)] = w[P];
    });
    var C = j(j({}, g), {}, {
      unitless: _,
      prefixToken: b
    }), v = f(d, h, y, C), x = u(p, y, C);
    return function(P) {
      var N = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : P, O = v(P, N), I = te(O, 2), T = I[1], A = x(N), L = te(A, 2), R = L[0], F = L[1];
      return [R, T, F];
    };
  }
  function u(d, h, y) {
    var g = y.unitless, p = y.injectStyle, b = p === void 0 ? !0 : p, w = y.prefixToken, E = y.ignore, _ = function(x) {
      var P = x.rootCls, N = x.cssVar, O = N === void 0 ? {} : N, I = r(), T = I.realToken;
      return li({
        path: [d],
        prefix: O.prefix,
        key: O.key,
        unitless: g,
        ignore: E,
        token: T,
        scope: P
      }, function() {
        var A = dr(d, T, h), L = ur(d, T, A, {
          deprecatedTokens: y == null ? void 0 : y.deprecatedTokens
        });
        return Object.keys(A).forEach(function(R) {
          L[w(R)] = L[R], delete L[R];
        }), L;
      }), null;
    }, C = function(x) {
      var P = r(), N = P.cssVar;
      return [function(O) {
        return b && N ? /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(_, {
          rootCls: x,
          cssVar: N,
          component: d
        }), O) : O;
      }, N == null ? void 0 : N.key];
    };
    return C;
  }
  function f(d, h, y) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = Array.isArray(d) ? d : [d, d], b = te(p, 1), w = b[0], E = p.join("-"), _ = e.layer || {
      name: "antd"
    };
    return function(C) {
      var v = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, x = r(), P = x.theme, N = x.realToken, O = x.hashId, I = x.token, T = x.cssVar, A = o(), L = A.rootPrefixCls, R = A.iconPrefixCls, F = n(), W = T ? "css" : "js", X = Ys(function() {
        var U = /* @__PURE__ */ new Set();
        return T && Object.keys(g.unitless || {}).forEach(function(oe) {
          U.add(Wt(oe, T.prefix)), U.add(Wt(oe, cr(w, T.prefix)));
        }), Ws(W, U);
      }, [W, w, T == null ? void 0 : T.prefix]), Y = Gs(W), B = Y.max, z = Y.min, K = {
        theme: P,
        token: I,
        hashId: O,
        nonce: function() {
          return F.nonce;
        },
        clientOnly: g.clientOnly,
        layer: _,
        // antd is always at top of styles
        order: g.order || -999
      };
      typeof i == "function" && An(j(j({}, K), {}, {
        clientOnly: !1,
        path: ["Shared", L]
      }), function() {
        return i(I, {
          prefix: {
            rootPrefixCls: L,
            iconPrefixCls: R
          },
          csp: F
        });
      });
      var J = An(j(j({}, K), {}, {
        path: [E, C, R]
      }), function() {
        if (g.injectStyle === !1)
          return [];
        var U = Us(I), oe = U.token, Ne = U.flush, ue = dr(w, N, y), qe = ".".concat(C), Fe = ur(w, N, ue, {
          deprecatedTokens: g.deprecatedTokens
        });
        T && ue && Z(ue) === "object" && Object.keys(ue).forEach(function(ke) {
          ue[ke] = "var(".concat(Wt(ke, cr(w, T.prefix)), ")");
        });
        var Oe = Ke(oe, {
          componentCls: qe,
          prefixCls: C,
          iconCls: ".".concat(R),
          antCls: ".".concat(L),
          calc: X,
          // @ts-ignore
          max: B,
          // @ts-ignore
          min: z
        }, T ? ue : Fe), je = h(Oe, {
          hashId: O,
          prefixCls: C,
          rootPrefixCls: L,
          iconPrefixCls: R
        });
        Ne(w, Fe);
        var be = typeof s == "function" ? s(Oe, C, v, g.resetFont) : null;
        return [g.resetStyle === !1 ? null : be, je];
      });
      return [J, O];
    };
  }
  function m(d, h, y) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = f(d, h, y, j({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, g)), b = function(E) {
      var _ = E.prefixCls, C = E.rootCls, v = C === void 0 ? _ : C;
      return p(_, v), null;
    };
    return b;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: m,
    genComponentStyleHook: f
  };
}
function Je(e) {
  "@babel/helpers - typeof";
  return Je = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Je(e);
}
function Js(e, t) {
  if (Je(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var r = n.call(e, t);
    if (Je(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function ea(e) {
  var t = Js(e, "string");
  return Je(t) == "symbol" ? t : t + "";
}
function le(e, t, n) {
  return (t = ea(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
const q = Math.round;
function Qt(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = n.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    r[o] = t(r[o] || 0, n[o] || "", o);
  return n[3] ? r[3] = n[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const pr = (e, t, n) => n === 0 ? e : e / 100;
function Ye(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class ye {
  constructor(t) {
    le(this, "isValid", !0), le(this, "r", 0), le(this, "g", 0), le(this, "b", 0), le(this, "a", 1), le(this, "_h", void 0), le(this, "_s", void 0), le(this, "_l", void 0), le(this, "_v", void 0), le(this, "_max", void 0), le(this, "_min", void 0), le(this, "_brightness", void 0);
    function n(r) {
      return r[0] in t && r[1] in t && r[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(i) {
        return r.startsWith(i);
      };
      const r = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : o("rgb") ? this.fromRgbString(r) : o("hsl") ? this.fromHslString(r) : (o("hsv") || o("hsb")) && this.fromHsvString(r);
    } else if (t instanceof ye)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = Ye(t.r), this.g = Ye(t.g), this.b = Ye(t.b), this.a = typeof t.a == "number" ? Ye(t.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(t);
    else if (n("hsv"))
      this.fromHsv(t);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(t));
  }
  // ======================= Setter =======================
  setR(t) {
    return this._sc("r", t);
  }
  setG(t) {
    return this._sc("g", t);
  }
  setB(t) {
    return this._sc("b", t);
  }
  setA(t) {
    return this._sc("a", t, 1);
  }
  setHue(t) {
    const n = this.toHsv();
    return n.h = t, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), r = t(this.g), o = t(this.b);
    return 0.2126 * n + 0.7152 * r + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = q(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._s = 0 : this._s = t / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(t = 10) {
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const r = this._c(t), o = n / 100, i = (a) => (r[a] - this[a]) * o + this[a], s = {
      r: q(i("r")),
      g: q(i("g")),
      b: q(i("b")),
      a: q(i("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(t = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, t);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(t = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, t);
  }
  onBackground(t) {
    const n = this._c(t), r = this.a + n.a * (1 - this.a), o = (i) => q((this[i] * this.a + n[i] * n.a * (1 - this.a)) / r);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
      a: r
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(t) {
    return this.r === t.r && this.g === t.g && this.b === t.b && this.a === t.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let t = "#";
    const n = (this.r || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const r = (this.g || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = q(this.a * 255).toString(16);
      t += i.length === 2 ? i : "0" + i;
    }
    return t;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const t = this.getHue(), n = q(this.getSaturation() * 100), r = q(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${r}%,${this.a})` : `hsl(${t},${n}%,${r}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(t, n, r) {
    const o = this.clone();
    return o[t] = Ye(n, r), o;
  }
  _c(t) {
    return new this.constructor(t);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(t) {
    const n = t.replace("#", "");
    function r(o, i) {
      return parseInt(n[o] + n[i || o], 16);
    }
    n.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = n[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = n[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: r,
    a: o
  }) {
    if (this._h = t % 360, this._s = n, this._l = r, this.a = typeof o == "number" ? o : 1, n <= 0) {
      const d = q(r * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const l = t / 60, u = (1 - Math.abs(2 * r - 1)) * n, f = u * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (i = u, s = f) : l >= 1 && l < 2 ? (i = f, s = u) : l >= 2 && l < 3 ? (s = u, a = f) : l >= 3 && l < 4 ? (s = f, a = u) : l >= 4 && l < 5 ? (i = f, a = u) : l >= 5 && l < 6 && (i = u, a = f);
    const m = r - u / 2;
    this.r = q((i + m) * 255), this.g = q((s + m) * 255), this.b = q((a + m) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: r,
    a: o
  }) {
    this._h = t % 360, this._s = n, this._v = r, this.a = typeof o == "number" ? o : 1;
    const i = q(r * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), l = s - a, u = q(r * (1 - n) * 255), f = q(r * (1 - n * l) * 255), m = q(r * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = m, this.b = u;
        break;
      case 1:
        this.r = f, this.b = u;
        break;
      case 2:
        this.r = u, this.b = m;
        break;
      case 3:
        this.r = u, this.g = f;
        break;
      case 4:
        this.r = m, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const n = Qt(t, pr);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = Qt(t, pr);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = Qt(t, (r, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? q(r / 100 * 255) : r
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const ta = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, na = Object.assign(Object.assign({}, ta), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function Zt(e) {
  return e >= 0 && e <= 255;
}
function ct(e, t) {
  const {
    r: n,
    g: r,
    b: o,
    a: i
  } = new ye(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: l
  } = new ye(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const f = Math.round((n - s * (1 - u)) / u), m = Math.round((r - a * (1 - u)) / u), d = Math.round((o - l * (1 - u)) / u);
    if (Zt(f) && Zt(m) && Zt(d))
      return new ye({
        r: f,
        g: m,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new ye({
    r: n,
    g: r,
    b: o,
    a: 1
  }).toRgbString();
}
var ra = function(e, t) {
  var n = {};
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
    t.indexOf(r[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, r[o]) && (n[r[o]] = e[r[o]]);
  return n;
};
function oa(e) {
  const {
    override: t
  } = e, n = ra(e, ["override"]), r = Object.assign({}, t);
  Object.keys(na).forEach((d) => {
    delete r[d];
  });
  const o = Object.assign(Object.assign({}, n), r), i = 480, s = 576, a = 768, l = 992, u = 1200, f = 1600;
  if (o.motion === !1) {
    const d = "0s";
    o.motionDurationFast = d, o.motionDurationMid = d, o.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, o), {
    // ============== Background ============== //
    colorFillContent: o.colorFillSecondary,
    colorFillContentHover: o.colorFill,
    colorFillAlter: o.colorFillQuaternary,
    colorBgContainerDisabled: o.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: o.colorBgContainer,
    colorSplit: ct(o.colorBorderSecondary, o.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: o.colorTextQuaternary,
    colorTextDisabled: o.colorTextQuaternary,
    colorTextHeading: o.colorText,
    colorTextLabel: o.colorTextSecondary,
    colorTextDescription: o.colorTextTertiary,
    colorTextLightSolid: o.colorWhite,
    colorHighlight: o.colorError,
    colorBgTextHover: o.colorFillSecondary,
    colorBgTextActive: o.colorFill,
    colorIcon: o.colorTextTertiary,
    colorIconHover: o.colorText,
    colorErrorOutline: ct(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: ct(o.colorWarningBg, o.colorBgContainer),
    // Font
    fontSizeIcon: o.fontSizeSM,
    // Line
    lineWidthFocus: o.lineWidth * 3,
    // Control
    lineWidth: o.lineWidth,
    controlOutlineWidth: o.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: o.controlHeight / 2,
    controlItemBgHover: o.colorFillTertiary,
    controlItemBgActive: o.colorPrimaryBg,
    controlItemBgActiveHover: o.colorPrimaryBgHover,
    controlItemBgActiveDisabled: o.colorFill,
    controlTmpOutline: o.colorFillQuaternary,
    controlOutline: ct(o.colorPrimaryBg, o.colorBgContainer),
    lineType: o.lineType,
    borderRadius: o.borderRadius,
    borderRadiusXS: o.borderRadiusXS,
    borderRadiusSM: o.borderRadiusSM,
    borderRadiusLG: o.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: o.sizeXXS,
    paddingXS: o.sizeXS,
    paddingSM: o.sizeSM,
    padding: o.size,
    paddingMD: o.sizeMD,
    paddingLG: o.sizeLG,
    paddingXL: o.sizeXL,
    paddingContentHorizontalLG: o.sizeLG,
    paddingContentVerticalLG: o.sizeMS,
    paddingContentHorizontal: o.sizeMS,
    paddingContentVertical: o.sizeSM,
    paddingContentHorizontalSM: o.size,
    paddingContentVerticalSM: o.sizeXS,
    marginXXS: o.sizeXXS,
    marginXS: o.sizeXS,
    marginSM: o.sizeSM,
    margin: o.size,
    marginMD: o.sizeMD,
    marginLG: o.sizeLG,
    marginXL: o.sizeXL,
    marginXXL: o.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: i,
    screenXSMin: i,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new ye("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new ye("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new ye("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), r);
}
const ia = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, sa = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, aa = ci(yt.defaultAlgorithm), la = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, ao = (e, t, n) => {
  const r = n.getDerivativeToken(e), {
    override: o,
    ...i
  } = t;
  let s = {
    ...r,
    override: o
  };
  return s = oa(s), i && Object.entries(i).forEach(([a, l]) => {
    const {
      theme: u,
      ...f
    } = l;
    let m = f;
    u && (m = ao({
      ...s,
      ...f
    }, {
      override: f
    }, u)), s[a] = m;
  }), s;
};
function ca() {
  const {
    token: e,
    hashed: t,
    theme: n = aa,
    override: r,
    cssVar: o
  } = c.useContext(yt._internalContext), [i, s, a] = ui(n, [yt.defaultSeed, e], {
    salt: `${Yi}-${t || ""}`,
    override: r,
    getComputedToken: ao,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: ia,
      ignore: sa,
      preserve: la
    }
  });
  return [n, a, t ? s : "", i, o];
}
const {
  genStyleHooks: At
} = Zs({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = $e();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, r, o] = ca();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: r,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = $e();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), ua = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list-card`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [r]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${r}-name,${r}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${r}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${r}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: n(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: n(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${r}-icon`]: {
          fontSize: n(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: n(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${r}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${r}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: o,
        height: o,
        lineHeight: 1,
        [`&:not(${r}-status-error)`]: {
          border: 0
        },
        // Img
        img: {
          width: "100%",
          height: "100%",
          verticalAlign: "top",
          objectFit: "cover",
          borderRadius: "inherit"
        },
        // Mask
        [`${r}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${r}-status-error`]: {
          [`img, ${r}-img-mask`]: {
            borderRadius: n(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${r}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${r}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${r}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: e.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: e.fontSize,
        cursor: "pointer",
        opacity: e.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: e.opacityLoading
        }
      },
      [`&:hover ${r}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${r}-desc`]: {
          color: e.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((i) => `${i} ${e.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: n(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, dn = {
  "&, *": {
    boxSizing: "border-box"
  }
}, fa = (e) => {
  const {
    componentCls: t,
    calc: n,
    antCls: r
  } = e, o = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...dn,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${i}-inner`]: {
          display: "none"
        }
      },
      [i]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [i]: {
        height: "100%",
        borderRadius: e.borderRadius,
        borderWidth: e.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: e.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: e.colorBgPlaceholderHover,
        ...dn,
        [`${r}-upload-wrapper ${r}-upload${r}-upload-btn`]: {
          padding: 0
        },
        [`&${i}-drag-in`]: {
          borderColor: e.colorPrimaryHover
        },
        [`&${i}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${i}-inner`]: {
          gap: n(e.paddingXXS).div(2).equal()
        },
        [`${i}-icon`]: {
          fontSize: e.fontSizeHeading2,
          lineHeight: 1
        },
        [`${i}-title${i}-title`]: {
          margin: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight
        },
        [`${i}-description`]: {}
      }
    }
  };
}, da = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...dn,
      // =============================== File List ===============================
      [r]: {
        display: "flex",
        flexWrap: "wrap",
        gap: e.paddingSM,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        color: e.colorText,
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        width: "100%",
        background: e.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${e.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: n(o).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: o,
          height: o,
          fontSize: e.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: e.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&:dir(ltr)": {
          [`&${r}-overflow-ping-start ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-end ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${r}-overflow-ping-end ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-start ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, ma = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new ye(t).setA(0.85).toRgbString()
  };
}, lo = At("Attachments", (e) => {
  const t = Ke(e, {});
  return [fa(t), da(t), ua(t)];
}, ma), pa = (e) => e.indexOf("image/") === 0, ut = 200;
function ga(e) {
  return new Promise((t) => {
    if (!e || !e.type || !pa(e.type)) {
      t("");
      return;
    }
    const n = new Image();
    if (n.onload = () => {
      const {
        width: r,
        height: o
      } = n, i = r / o, s = i > 1 ? ut : ut * i, a = i > 1 ? ut / i : ut, l = document.createElement("canvas");
      l.width = s, l.height = a, l.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(l), l.getContext("2d").drawImage(n, 0, 0, s, a);
      const f = l.toDataURL();
      document.body.removeChild(l), window.URL.revokeObjectURL(n.src), t(f);
    }, n.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (n.src = r.result);
      }, r.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && t(r.result);
      }, r.readAsDataURL(e);
    } else
      n.src = window.URL.createObjectURL(e);
  });
}
function ha() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "audio"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function ya(e) {
  const {
    percent: t
  } = e, {
    token: n
  } = yt.useToken();
  return /* @__PURE__ */ c.createElement(ti, {
    type: "circle",
    percent: t,
    size: n.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ c.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function va() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "video"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const Jt = " ", mn = "#8c8c8c", co = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], ba = [{
  icon: /* @__PURE__ */ c.createElement(jo, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ c.createElement(ko, null),
  color: mn,
  ext: co
}, {
  icon: /* @__PURE__ */ c.createElement(Ao, null),
  color: mn,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ c.createElement(zo, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ c.createElement(Do, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Ho, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Bo, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ c.createElement(va, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ c.createElement(ha, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function gr(e, t) {
  return t.some((n) => e.toLowerCase() === `.${n}`);
}
function Sa(e) {
  let t = e;
  const n = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; t >= 1024 && r < n.length - 1; )
    t /= 1024, r++;
  return `${t.toFixed(0)} ${n[r]}`;
}
function xa(e, t) {
  const {
    prefixCls: n,
    item: r,
    onRemove: o,
    className: i,
    style: s
  } = e, a = c.useContext(nt), {
    disabled: l
  } = a || {}, {
    name: u,
    size: f,
    percent: m,
    status: d = "done",
    description: h
  } = r, {
    getPrefixCls: y
  } = $e(), g = y("attachment", n), p = `${g}-list-card`, [b, w, E] = lo(g), [_, C] = c.useMemo(() => {
    const R = u || "", F = R.match(/^(.*)\.[^.]+$/);
    return F ? [F[1], R.slice(F[1].length)] : [R, ""];
  }, [u]), v = c.useMemo(() => gr(C, co), [C]), x = c.useMemo(() => h || (d === "uploading" ? `${m || 0}%` : d === "error" ? r.response || Jt : f ? Sa(f) : Jt), [d, m]), [P, N] = c.useMemo(() => {
    for (const {
      ext: R,
      icon: F,
      color: W
    } of ba)
      if (gr(C, R))
        return [F, W];
    return [/* @__PURE__ */ c.createElement(Fo, {
      key: "defaultIcon"
    }), mn];
  }, [C]), [O, I] = c.useState();
  c.useEffect(() => {
    if (r.originFileObj) {
      let R = !0;
      return ga(r.originFileObj).then((F) => {
        R && I(F);
      }), () => {
        R = !1;
      };
    }
    I(void 0);
  }, [r.originFileObj]);
  let T = null;
  const A = r.thumbUrl || r.url || O, L = v && (r.originFileObj || A);
  return L ? T = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement("img", {
    alt: "preview",
    src: A
  }), d !== "done" && /* @__PURE__ */ c.createElement("div", {
    className: `${p}-img-mask`
  }, d === "uploading" && m !== void 0 && /* @__PURE__ */ c.createElement(ya, {
    percent: m,
    prefixCls: p
  }), d === "error" && /* @__PURE__ */ c.createElement("div", {
    className: `${p}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-ellipsis-prefix`
  }, x)))) : T = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-icon`,
    style: {
      color: N
    }
  }, P), /* @__PURE__ */ c.createElement("div", {
    className: `${p}-content`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-name`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-ellipsis-prefix`
  }, _ ?? Jt), /* @__PURE__ */ c.createElement("div", {
    className: `${p}-ellipsis-suffix`
  }, C)), /* @__PURE__ */ c.createElement("div", {
    className: `${p}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-ellipsis-prefix`
  }, x)))), b(/* @__PURE__ */ c.createElement("div", {
    className: k(p, {
      [`${p}-status-${d}`]: d,
      [`${p}-type-preview`]: L,
      [`${p}-type-overview`]: !L
    }, i, w, E),
    style: s,
    ref: t
  }, T, !l && o && /* @__PURE__ */ c.createElement("button", {
    type: "button",
    className: `${p}-remove`,
    onClick: () => {
      o(r);
    }
  }, /* @__PURE__ */ c.createElement(Oo, null))));
}
const uo = /* @__PURE__ */ c.forwardRef(xa), hr = 1;
function wa(e) {
  const {
    prefixCls: t,
    items: n,
    onRemove: r,
    overflow: o,
    upload: i,
    listClassName: s,
    listStyle: a,
    itemClassName: l,
    itemStyle: u
  } = e, f = `${t}-list`, m = c.useRef(null), [d, h] = c.useState(!1), {
    disabled: y
  } = c.useContext(nt);
  c.useEffect(() => (h(!0), () => {
    h(!1);
  }), []);
  const [g, p] = c.useState(!1), [b, w] = c.useState(!1), E = () => {
    const x = m.current;
    x && (o === "scrollX" ? (p(Math.abs(x.scrollLeft) >= hr), w(x.scrollWidth - x.clientWidth - Math.abs(x.scrollLeft) >= hr)) : o === "scrollY" && (p(x.scrollTop !== 0), w(x.scrollHeight - x.clientHeight !== x.scrollTop)));
  };
  c.useEffect(() => {
    E();
  }, [o]);
  const _ = (x) => {
    const P = m.current;
    P && P.scrollTo({
      left: P.scrollLeft + x * P.clientWidth,
      behavior: "smooth"
    });
  }, C = () => {
    _(-1);
  }, v = () => {
    _(1);
  };
  return /* @__PURE__ */ c.createElement("div", {
    className: k(f, {
      [`${f}-overflow-${e.overflow}`]: o,
      [`${f}-overflow-ping-start`]: g,
      [`${f}-overflow-ping-end`]: b
    }, s),
    ref: m,
    onScroll: E,
    style: a
  }, /* @__PURE__ */ c.createElement(zs, {
    keys: n.map((x) => ({
      key: x.uid,
      item: x
    })),
    motionName: `${f}-card-motion`,
    component: !1,
    motionAppear: d,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: x,
    item: P,
    className: N,
    style: O
  }) => /* @__PURE__ */ c.createElement(uo, {
    key: x,
    prefixCls: t,
    item: P,
    onRemove: r,
    className: k(N, l),
    style: {
      ...O,
      ...u
    }
  })), !y && /* @__PURE__ */ c.createElement(ro, {
    upload: i
  }, /* @__PURE__ */ c.createElement(ie, {
    className: `${f}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ c.createElement(Vo, {
    className: `${f}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(ie, {
    size: "small",
    shape: "circle",
    className: `${f}-prev-btn`,
    icon: /* @__PURE__ */ c.createElement(Wo, null),
    onClick: C
  }), /* @__PURE__ */ c.createElement(ie, {
    size: "small",
    shape: "circle",
    className: `${f}-next-btn`,
    icon: /* @__PURE__ */ c.createElement(Xo, null),
    onClick: v
  })));
}
function _a(e, t) {
  const {
    prefixCls: n,
    placeholder: r = {},
    upload: o,
    className: i,
    style: s
  } = e, a = `${n}-placeholder`, l = r || {}, {
    disabled: u
  } = c.useContext(nt), [f, m] = c.useState(!1), d = () => {
    m(!0);
  }, h = (p) => {
    p.currentTarget.contains(p.relatedTarget) || m(!1);
  }, y = () => {
    m(!1);
  }, g = /* @__PURE__ */ c.isValidElement(r) ? r : /* @__PURE__ */ c.createElement(_e, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ c.createElement(Te.Text, {
    className: `${a}-icon`
  }, l.icon), /* @__PURE__ */ c.createElement(Te.Title, {
    className: `${a}-title`,
    level: 5
  }, l.title), /* @__PURE__ */ c.createElement(Te.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, l.description));
  return /* @__PURE__ */ c.createElement("div", {
    className: k(a, {
      [`${a}-drag-in`]: f,
      [`${a}-disabled`]: u
    }, i),
    onDragEnter: d,
    onDragLeave: h,
    onDrop: y,
    "aria-hidden": u,
    style: s
  }, /* @__PURE__ */ c.createElement(Ir.Dragger, Ce({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), g));
}
const Ca = /* @__PURE__ */ c.forwardRef(_a);
function Ea(e, t) {
  const {
    prefixCls: n,
    rootClassName: r,
    rootStyle: o,
    className: i,
    style: s,
    items: a,
    children: l,
    getDropContainer: u,
    placeholder: f,
    onChange: m,
    overflow: d,
    disabled: h,
    classNames: y = {},
    styles: g = {},
    ...p
  } = e, {
    getPrefixCls: b,
    direction: w
  } = $e(), E = b("attachment", n), _ = Ct("attachments"), {
    classNames: C,
    styles: v
  } = _, x = c.useRef(null), P = c.useRef(null);
  c.useImperativeHandle(t, () => ({
    nativeElement: x.current,
    upload: (B) => {
      var K, J;
      const z = (J = (K = P.current) == null ? void 0 : K.nativeElement) == null ? void 0 : J.querySelector('input[type="file"]');
      if (z) {
        const U = new DataTransfer();
        U.items.add(B), z.files = U.files, z.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [N, O, I] = lo(E), T = k(O, I), [A, L] = rs([], {
    value: a
  }), R = Pe((B) => {
    L(B.fileList), m == null || m(B);
  }), F = {
    ...p,
    fileList: A,
    onChange: R
  }, W = (B) => {
    const z = A.filter((K) => K.uid !== B.uid);
    R({
      file: B,
      fileList: z
    });
  };
  let X;
  const Y = (B, z, K) => {
    const J = typeof f == "function" ? f(B) : f;
    return /* @__PURE__ */ c.createElement(Ca, {
      placeholder: J,
      upload: F,
      prefixCls: E,
      className: k(C.placeholder, y.placeholder),
      style: {
        ...v.placeholder,
        ...g.placeholder,
        ...z == null ? void 0 : z.style
      },
      ref: K
    });
  };
  if (l)
    X = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(ro, {
      upload: F,
      rootClassName: r,
      ref: P
    }, l), /* @__PURE__ */ c.createElement(Jn, {
      getDropContainer: u,
      prefixCls: E,
      className: k(T, r)
    }, Y("drop")));
  else {
    const B = A.length > 0;
    X = /* @__PURE__ */ c.createElement("div", {
      className: k(E, T, {
        [`${E}-rtl`]: w === "rtl"
      }, i, r),
      style: {
        ...o,
        ...s
      },
      dir: w || "ltr",
      ref: x
    }, /* @__PURE__ */ c.createElement(wa, {
      prefixCls: E,
      items: A,
      onRemove: W,
      overflow: d,
      upload: F,
      listClassName: k(C.list, y.list),
      listStyle: {
        ...v.list,
        ...g.list,
        ...!B && {
          display: "none"
        }
      },
      itemClassName: k(C.item, y.item),
      itemStyle: {
        ...v.item,
        ...g.item
      }
    }), Y("inline", B ? {
      style: {
        display: "none"
      }
    } : {}, P), /* @__PURE__ */ c.createElement(Jn, {
      getDropContainer: u || (() => x.current),
      prefixCls: E,
      className: T
    }, Y("drop")));
  }
  return N(/* @__PURE__ */ c.createElement(nt.Provider, {
    value: {
      disabled: h
    }
  }, X));
}
const fo = /* @__PURE__ */ c.forwardRef(Ea);
fo.FileCard = uo;
var Ta = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, $a = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Pa = "".concat(Ta, " ").concat($a).split(/[\s\n]+/), Ra = "aria-", Ia = "data-";
function yr(e, t) {
  return e.indexOf(t) === 0;
}
function Ma(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = j({}, t);
  var r = {};
  return Object.keys(e).forEach(function(o) {
    // Aria
    (n.aria && (o === "role" || yr(o, Ra)) || // Data
    n.data && yr(o, Ia) || // Attr
    n.attr && Pa.includes(o)) && (r[o] = e[o]);
  }), r;
}
function ft(e) {
  return typeof e == "string";
}
const La = (e, t, n, r) => {
  const [o, i] = M.useState(""), [s, a] = M.useState(1), l = t && ft(e);
  return zr(() => {
    i(e), !l && ft(e) ? a(e.length) : ft(e) && ft(o) && e.indexOf(o) !== 0 && a(1);
  }, [e]), M.useEffect(() => {
    if (l && s < e.length) {
      const f = setTimeout(() => {
        a((m) => m + n);
      }, r);
      return () => {
        clearTimeout(f);
      };
    }
  }, [s, t, e]), [l ? e.slice(0, s) : e, l && s < e.length];
};
function Na(e) {
  return M.useMemo(() => {
    if (!e)
      return [!1, 0, 0, null];
    let t = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof e == "object" && (t = {
      ...t,
      ...e
    }), [!0, t.step, t.interval, t.suffix];
  }, [e]);
}
const Fa = ({
  prefixCls: e
}) => /* @__PURE__ */ c.createElement("span", {
  className: `${e}-dot`
}, /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-3"
})), Oa = (e) => {
  const {
    componentCls: t,
    paddingSM: n,
    padding: r
  } = e;
  return {
    [t]: {
      [`${t}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${Ve(n)} ${Ve(r)}`,
          borderRadius: e.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: e.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${e.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: e.boxShadowTertiary
        }
      }
    }
  };
}, ja = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: r,
    paddingSM: o,
    padding: i,
    calc: s
  } = e, a = s(n).mul(r).div(2).add(o).equal(), l = `${t}-content`;
  return {
    [t]: {
      [l]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: s(i).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${l}-corner`]: {
        borderStartStartRadius: e.borderRadiusXS
      },
      [`&-end ${l}-corner`]: {
        borderStartEndRadius: e.borderRadiusXS
      }
    }
  };
}, ka = (e) => {
  const {
    componentCls: t,
    padding: n
  } = e;
  return {
    [`${t}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: n,
      overflowY: "auto"
    }
  };
}, Aa = new Lr("loadingMove", {
  "0%": {
    transform: "translateY(0)"
  },
  "10%": {
    transform: "translateY(4px)"
  },
  "20%": {
    transform: "translateY(0)"
  },
  "30%": {
    transform: "translateY(-4px)"
  },
  "40%": {
    transform: "translateY(0)"
  }
}), za = new Lr("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), Da = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: r,
    paddingSM: o,
    colorText: i,
    calc: s
  } = e;
  return {
    [t]: {
      display: "flex",
      columnGap: o,
      [`&${t}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${t}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`&${t}-typing ${t}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: za,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${t}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${t}-header, & ${t}-footer`]: {
        fontSize: n,
        lineHeight: r,
        color: e.colorText
      },
      [`& ${t}-header`]: {
        marginBottom: e.paddingXXS
      },
      [`& ${t}-footer`]: {
        marginTop: o
      },
      // =========================== Content =============================
      [`& ${t}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${t}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: i,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        minHeight: s(o).mul(2).add(s(r).mul(n)).equal(),
        wordBreak: "break-word",
        [`& ${t}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: e.marginXS,
          padding: `0 ${Ve(e.paddingXXS)}`,
          "&-item": {
            backgroundColor: e.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: Aa,
            animationDuration: "2s",
            animationIterationCount: "infinite",
            animationTimingFunction: "linear",
            "&:nth-child(1)": {
              animationDelay: "0s"
            },
            "&:nth-child(2)": {
              animationDelay: "0.2s"
            },
            "&:nth-child(3)": {
              animationDelay: "0.4s"
            }
          }
        }
      }
    }
  };
}, Ha = () => ({}), mo = At("Bubble", (e) => {
  const t = Ke(e, {});
  return [Da(t), ka(t), Oa(t), ja(t)];
}, Ha), po = /* @__PURE__ */ c.createContext({}), Ba = (e, t) => {
  const {
    prefixCls: n,
    className: r,
    rootClassName: o,
    style: i,
    classNames: s = {},
    styles: a = {},
    avatar: l,
    placement: u = "start",
    loading: f = !1,
    loadingRender: m,
    typing: d,
    content: h = "",
    messageRender: y,
    variant: g = "filled",
    shape: p,
    onTypingComplete: b,
    header: w,
    footer: E,
    ..._
  } = e, {
    onUpdate: C
  } = c.useContext(po), v = c.useRef(null);
  c.useImperativeHandle(t, () => ({
    nativeElement: v.current
  }));
  const {
    direction: x,
    getPrefixCls: P
  } = $e(), N = P("bubble", n), O = Ct("bubble"), [I, T, A, L] = Na(d), [R, F] = La(h, I, T, A);
  c.useEffect(() => {
    C == null || C();
  }, [R]);
  const W = c.useRef(!1);
  c.useEffect(() => {
    !F && !f ? W.current || (W.current = !0, b == null || b()) : W.current = !1;
  }, [F, f]);
  const [X, Y, B] = mo(N), z = k(N, o, O.className, r, Y, B, `${N}-${u}`, {
    [`${N}-rtl`]: x === "rtl",
    [`${N}-typing`]: F && !f && !y && !L
  }), K = /* @__PURE__ */ c.isValidElement(l) ? l : /* @__PURE__ */ c.createElement(ni, l), J = y ? y(R) : R;
  let U;
  f ? U = m ? m() : /* @__PURE__ */ c.createElement(Fa, {
    prefixCls: N
  }) : U = /* @__PURE__ */ c.createElement(c.Fragment, null, J, F && L);
  let oe = /* @__PURE__ */ c.createElement("div", {
    style: {
      ...O.styles.content,
      ...a.content
    },
    className: k(`${N}-content`, `${N}-content-${g}`, p && `${N}-content-${p}`, O.classNames.content, s.content)
  }, U);
  return (w || E) && (oe = /* @__PURE__ */ c.createElement("div", {
    className: `${N}-content-wrapper`
  }, w && /* @__PURE__ */ c.createElement("div", {
    className: k(`${N}-header`, O.classNames.header, s.header),
    style: {
      ...O.styles.header,
      ...a.header
    }
  }, w), oe, E && /* @__PURE__ */ c.createElement("div", {
    className: k(`${N}-footer`, O.classNames.footer, s.footer),
    style: {
      ...O.styles.footer,
      ...a.footer
    }
  }, E))), X(/* @__PURE__ */ c.createElement("div", Ce({
    style: {
      ...O.style,
      ...i
    },
    className: z
  }, _, {
    ref: v
  }), l && /* @__PURE__ */ c.createElement("div", {
    style: {
      ...O.styles.avatar,
      ...a.avatar
    },
    className: k(`${N}-avatar`, O.classNames.avatar, s.avatar)
  }, K), oe));
}, $n = /* @__PURE__ */ c.forwardRef(Ba);
function Va(e) {
  const [t, n] = c.useState(e.length), r = c.useMemo(() => e.slice(0, t), [e, t]), o = c.useMemo(() => {
    const s = r[r.length - 1];
    return s ? s.key : null;
  }, [r]);
  c.useEffect(() => {
    var s;
    if (!(r.length && r.every((a, l) => {
      var u;
      return a.key === ((u = e[l]) == null ? void 0 : u.key);
    }))) {
      if (r.length === 0)
        n(1);
      else
        for (let a = 0; a < r.length; a += 1)
          if (r[a].key !== ((s = e[a]) == null ? void 0 : s.key)) {
            n(a);
            break;
          }
    }
  }, [e]);
  const i = Pe((s) => {
    s === o && n(t + 1);
  });
  return [r, i];
}
function Wa(e, t) {
  const n = M.useCallback((r) => typeof t == "function" ? t(r) : t ? t[r.role] || {} : {}, [t]);
  return M.useMemo(() => (e || []).map((r, o) => {
    const i = r.key ?? `preset_${o}`;
    return {
      ...n(r),
      ...r,
      key: i
    };
  }), [e, n]);
}
const Xa = 1, Ua = (e, t) => {
  const {
    prefixCls: n,
    rootClassName: r,
    className: o,
    items: i,
    autoScroll: s = !0,
    roles: a,
    ...l
  } = e, u = Ma(l, {
    attr: !0,
    aria: !0
  }), f = M.useRef(null), m = M.useRef({}), {
    getPrefixCls: d
  } = $e(), h = d("bubble", n), y = `${h}-list`, [g, p, b] = mo(h), [w, E] = M.useState(!1);
  M.useEffect(() => (E(!0), () => {
    E(!1);
  }), []);
  const _ = Wa(i, a), [C, v] = Va(_), [x, P] = M.useState(!0), [N, O] = M.useState(0), I = (L) => {
    const R = L.target;
    P(R.scrollHeight - Math.abs(R.scrollTop) - R.clientHeight <= Xa);
  };
  M.useEffect(() => {
    s && f.current && x && f.current.scrollTo({
      top: f.current.scrollHeight
    });
  }, [N]), M.useEffect(() => {
    var L;
    if (s) {
      const R = (L = C[C.length - 2]) == null ? void 0 : L.key, F = m.current[R];
      if (F) {
        const {
          nativeElement: W
        } = F, {
          top: X,
          bottom: Y
        } = W.getBoundingClientRect(), {
          top: B,
          bottom: z
        } = f.current.getBoundingClientRect();
        X < z && Y > B && (O((J) => J + 1), P(!0));
      }
    }
  }, [C.length]), M.useImperativeHandle(t, () => ({
    nativeElement: f.current,
    scrollTo: ({
      key: L,
      offset: R,
      behavior: F = "smooth",
      block: W
    }) => {
      if (typeof R == "number")
        f.current.scrollTo({
          top: R,
          behavior: F
        });
      else if (L !== void 0) {
        const X = m.current[L];
        if (X) {
          const Y = C.findIndex((B) => B.key === L);
          P(Y === C.length - 1), X.nativeElement.scrollIntoView({
            behavior: F,
            block: W
          });
        }
      }
    }
  }));
  const T = Pe(() => {
    s && O((L) => L + 1);
  }), A = M.useMemo(() => ({
    onUpdate: T
  }), []);
  return g(/* @__PURE__ */ M.createElement(po.Provider, {
    value: A
  }, /* @__PURE__ */ M.createElement("div", Ce({}, u, {
    className: k(y, r, o, p, b, {
      [`${y}-reach-end`]: x
    }),
    ref: f,
    onScroll: I
  }), C.map(({
    key: L,
    ...R
  }) => /* @__PURE__ */ M.createElement($n, Ce({}, R, {
    key: L,
    ref: (F) => {
      F ? m.current[L] = F : delete m.current[L];
    },
    typing: w ? R.typing : !1,
    onTypingComplete: () => {
      var F;
      (F = R.onTypingComplete) == null || F.call(R), v(L);
    }
  }))))));
}, Ga = /* @__PURE__ */ M.forwardRef(Ua);
$n.List = Ga;
const Ka = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ======================== Prompt ========================
      "&, & *": {
        boxSizing: "border-box"
      },
      maxWidth: "100%",
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`& ${t}-title`]: {
        marginBlockStart: 0,
        fontWeight: "normal",
        color: e.colorTextTertiary
      },
      [`& ${t}-list`]: {
        display: "flex",
        gap: e.paddingSM,
        overflowX: "scroll",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        listStyle: "none",
        paddingInlineStart: 0,
        marginBlock: 0,
        alignItems: "stretch",
        "&-wrap": {
          flexWrap: "wrap"
        },
        "&-vertical": {
          flexDirection: "column",
          alignItems: "flex-start"
        }
      },
      // ========================= Item =========================
      [`${t}-item`]: {
        flex: "none",
        display: "flex",
        gap: e.paddingXS,
        height: "auto",
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        alignItems: "flex-start",
        justifyContent: "flex-start",
        background: e.colorBgContainer,
        borderRadius: e.borderRadiusLG,
        transition: ["border", "background"].map((n) => `${n} ${e.motionDurationSlow}`).join(","),
        border: `${Ve(e.lineWidth)} ${e.lineType} ${e.colorBorderSecondary}`,
        [`&:not(${t}-item-has-nest)`]: {
          "&:hover": {
            cursor: "pointer",
            background: e.colorFillTertiary
          },
          "&:active": {
            background: e.colorFill
          }
        },
        [`${t}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          gap: e.paddingXXS,
          flexDirection: "column",
          alignItems: "flex-start"
        },
        [`${t}-icon, ${t}-label, ${t}-desc`]: {
          margin: 0,
          padding: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight,
          textAlign: "start",
          whiteSpace: "normal"
        },
        [`${t}-label`]: {
          color: e.colorTextHeading,
          fontWeight: 500
        },
        [`${t}-label + ${t}-desc`]: {
          color: e.colorTextTertiary
        },
        // Disabled
        [`&${t}-item-disabled`]: {
          pointerEvents: "none",
          background: e.colorBgContainerDisabled,
          [`${t}-label, ${t}-desc`]: {
            color: e.colorTextTertiary
          }
        }
      }
    }
  };
}, qa = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ========================= Parent =========================
      [`${t}-item-has-nest`]: {
        [`> ${t}-content`]: {
          // gap: token.paddingSM,
          [`> ${t}-label`]: {
            fontSize: e.fontSizeLG,
            lineHeight: e.lineHeightLG
          }
        }
      },
      // ========================= Nested =========================
      [`&${t}-nested`]: {
        marginTop: e.paddingXS,
        // ======================== Prompt ========================
        alignSelf: "stretch",
        [`${t}-list`]: {
          alignItems: "stretch"
        },
        // ========================= Item =========================
        [`${t}-item`]: {
          border: 0,
          background: e.colorFillQuaternary
        }
      }
    }
  };
}, Ya = () => ({}), Qa = At("Prompts", (e) => {
  const t = Ke(e, {});
  return [Ka(t), qa(t)];
}, Ya), Pn = (e) => {
  const {
    prefixCls: t,
    title: n,
    className: r,
    items: o,
    onItemClick: i,
    vertical: s,
    wrap: a,
    rootClassName: l,
    styles: u = {},
    classNames: f = {},
    style: m,
    ...d
  } = e, {
    getPrefixCls: h,
    direction: y
  } = $e(), g = h("prompts", t), p = Ct("prompts"), [b, w, E] = Qa(g), _ = k(g, p.className, r, l, w, E, {
    [`${g}-rtl`]: y === "rtl"
  }), C = k(`${g}-list`, p.classNames.list, f.list, {
    [`${g}-list-wrap`]: a
  }, {
    [`${g}-list-vertical`]: s
  });
  return b(/* @__PURE__ */ c.createElement("div", Ce({}, d, {
    className: _,
    style: {
      ...m,
      ...p.style
    }
  }), n && /* @__PURE__ */ c.createElement(Te.Title, {
    level: 5,
    className: k(`${g}-title`, p.classNames.title, f.title),
    style: {
      ...p.styles.title,
      ...u.title
    }
  }, n), /* @__PURE__ */ c.createElement("div", {
    className: C,
    style: {
      ...p.styles.list,
      ...u.list
    }
  }, o == null ? void 0 : o.map((v, x) => {
    const P = v.children && v.children.length > 0;
    return /* @__PURE__ */ c.createElement("div", {
      key: v.key || `key_${x}`,
      style: {
        ...p.styles.item,
        ...u.item
      },
      className: k(`${g}-item`, p.classNames.item, f.item, {
        [`${g}-item-disabled`]: v.disabled,
        [`${g}-item-has-nest`]: P
      }),
      onClick: () => {
        !P && i && i({
          data: v
        });
      }
    }, v.icon && /* @__PURE__ */ c.createElement("div", {
      className: `${g}-icon`
    }, v.icon), /* @__PURE__ */ c.createElement("div", {
      className: k(`${g}-content`, p.classNames.itemContent, f.itemContent),
      style: {
        ...p.styles.itemContent,
        ...u.itemContent
      }
    }, v.label && /* @__PURE__ */ c.createElement("h6", {
      className: `${g}-label`
    }, v.label), v.description && /* @__PURE__ */ c.createElement("p", {
      className: `${g}-desc`
    }, v.description), P && /* @__PURE__ */ c.createElement(Pn, {
      className: `${g}-nested`,
      items: v.children,
      vertical: !0,
      onItemClick: i,
      classNames: {
        list: f.subList,
        item: f.subItem
      },
      styles: {
        list: u.subList,
        item: u.subItem
      }
    })));
  }))));
}, Za = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = n(e.fontSizeHeading3).mul(e.lineHeightHeading3).equal(), o = n(e.fontSize).mul(e.lineHeight).equal();
  return {
    [t]: {
      gap: e.padding,
      // ======================== Icon ========================
      [`${t}-icon`]: {
        height: n(r).add(o).add(e.paddingXXS).equal(),
        display: "flex",
        img: {
          height: "100%"
        }
      },
      // ==================== Content Wrap ====================
      [`${t}-content-wrapper`]: {
        gap: e.paddingXS,
        flex: "auto",
        minWidth: 0,
        [`${t}-title-wrapper`]: {
          gap: e.paddingXS
        },
        [`${t}-title`]: {
          margin: 0
        },
        [`${t}-extra`]: {
          marginInlineStart: "auto"
        }
      }
    }
  };
}, Ja = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ======================== Filled ========================
      "&-filled": {
        paddingInline: e.padding,
        paddingBlock: e.paddingSM,
        background: e.colorFillContent,
        borderRadius: e.borderRadiusLG
      },
      // ====================== Borderless ======================
      "&-borderless": {
        [`${t}-title`]: {
          fontSize: e.fontSizeHeading3,
          lineHeight: e.lineHeightHeading3
        }
      }
    }
  };
}, el = () => ({}), tl = At("Welcome", (e) => {
  const t = Ke(e, {});
  return [Za(t), Ja(t)];
}, el);
function nl(e, t) {
  const {
    prefixCls: n,
    rootClassName: r,
    className: o,
    style: i,
    variant: s = "filled",
    // Semantic
    classNames: a = {},
    styles: l = {},
    // Layout
    icon: u,
    title: f,
    description: m,
    extra: d
  } = e, {
    direction: h,
    getPrefixCls: y
  } = $e(), g = y("welcome", n), p = Ct("welcome"), [b, w, E] = tl(g), _ = c.useMemo(() => {
    if (!u)
      return null;
    let x = u;
    return typeof u == "string" && u.startsWith("http") && (x = /* @__PURE__ */ c.createElement("img", {
      src: u,
      alt: "icon"
    })), /* @__PURE__ */ c.createElement("div", {
      className: k(`${g}-icon`, p.classNames.icon, a.icon),
      style: l.icon
    }, x);
  }, [u]), C = c.useMemo(() => f ? /* @__PURE__ */ c.createElement(Te.Title, {
    level: 4,
    className: k(`${g}-title`, p.classNames.title, a.title),
    style: l.title
  }, f) : null, [f]), v = c.useMemo(() => d ? /* @__PURE__ */ c.createElement("div", {
    className: k(`${g}-extra`, p.classNames.extra, a.extra),
    style: l.extra
  }, d) : null, [d]);
  return b(/* @__PURE__ */ c.createElement(_e, {
    ref: t,
    className: k(g, p.className, o, r, w, E, `${g}-${s}`, {
      [`${g}-rtl`]: h === "rtl"
    }),
    style: i
  }, _, /* @__PURE__ */ c.createElement(_e, {
    vertical: !0,
    className: `${g}-content-wrapper`
  }, d ? /* @__PURE__ */ c.createElement(_e, {
    align: "flex-start",
    className: `${g}-title-wrapper`
  }, C, v) : C, m && /* @__PURE__ */ c.createElement(Te.Text, {
    className: k(`${g}-description`, p.classNames.description, a.description),
    style: l.description
  }, m))));
}
const rl = /* @__PURE__ */ c.forwardRef(nl);
function ne(e) {
  const t = Q(e);
  return t.current = e, Po((...n) => {
    var r;
    return (r = t.current) == null ? void 0 : r.call(t, ...n);
  }, []);
}
function he(e, t) {
  return Object.keys(e).reduce((n, r) => (e[r] !== void 0 && (!(t != null && t.omitNull) || e[r] !== null) && (n[r] = e[r]), n), {});
}
var go = Symbol.for("immer-nothing"), vr = Symbol.for("immer-draftable"), se = Symbol.for("immer-state");
function me(e, ...t) {
  throw new Error(`[Immer] minified error nr: ${e}. Full error at: https://bit.ly/3cXEKWf`);
}
var We = Object.getPrototypeOf;
function Xe(e) {
  return !!e && !!e[se];
}
function Me(e) {
  var t;
  return e ? ho(e) || Array.isArray(e) || !!e[vr] || !!((t = e.constructor) != null && t[vr]) || Dt(e) || Ht(e) : !1;
}
var ol = Object.prototype.constructor.toString();
function ho(e) {
  if (!e || typeof e != "object") return !1;
  const t = We(e);
  if (t === null)
    return !0;
  const n = Object.hasOwnProperty.call(t, "constructor") && t.constructor;
  return n === Object ? !0 : typeof n == "function" && Function.toString.call(n) === ol;
}
function St(e, t) {
  zt(e) === 0 ? Reflect.ownKeys(e).forEach((n) => {
    t(n, e[n], e);
  }) : e.forEach((n, r) => t(r, n, e));
}
function zt(e) {
  const t = e[se];
  return t ? t.type_ : Array.isArray(e) ? 1 : Dt(e) ? 2 : Ht(e) ? 3 : 0;
}
function pn(e, t) {
  return zt(e) === 2 ? e.has(t) : Object.prototype.hasOwnProperty.call(e, t);
}
function yo(e, t, n) {
  const r = zt(e);
  r === 2 ? e.set(t, n) : r === 3 ? e.add(n) : e[t] = n;
}
function il(e, t) {
  return e === t ? e !== 0 || 1 / e === 1 / t : e !== e && t !== t;
}
function Dt(e) {
  return e instanceof Map;
}
function Ht(e) {
  return e instanceof Set;
}
function Re(e) {
  return e.copy_ || e.base_;
}
function gn(e, t) {
  if (Dt(e))
    return new Map(e);
  if (Ht(e))
    return new Set(e);
  if (Array.isArray(e)) return Array.prototype.slice.call(e);
  const n = ho(e);
  if (t === !0 || t === "class_only" && !n) {
    const r = Object.getOwnPropertyDescriptors(e);
    delete r[se];
    let o = Reflect.ownKeys(r);
    for (let i = 0; i < o.length; i++) {
      const s = o[i], a = r[s];
      a.writable === !1 && (a.writable = !0, a.configurable = !0), (a.get || a.set) && (r[s] = {
        configurable: !0,
        writable: !0,
        // could live with !!desc.set as well here...
        enumerable: a.enumerable,
        value: e[s]
      });
    }
    return Object.create(We(e), r);
  } else {
    const r = We(e);
    if (r !== null && n)
      return {
        ...e
      };
    const o = Object.create(r);
    return Object.assign(o, e);
  }
}
function Rn(e, t = !1) {
  return Bt(e) || Xe(e) || !Me(e) || (zt(e) > 1 && (e.set = e.add = e.clear = e.delete = sl), Object.freeze(e), t && Object.entries(e).forEach(([n, r]) => Rn(r, !0))), e;
}
function sl() {
  me(2);
}
function Bt(e) {
  return Object.isFrozen(e);
}
var al = {};
function Le(e) {
  const t = al[e];
  return t || me(0, e), t;
}
var et;
function vo() {
  return et;
}
function ll(e, t) {
  return {
    drafts_: [],
    parent_: e,
    immer_: t,
    // Whenever the modified draft contains a draft from another scope, we
    // need to prevent auto-freezing so the unowned draft can be finalized.
    canAutoFreeze_: !0,
    unfinalizedDrafts_: 0
  };
}
function br(e, t) {
  t && (Le("Patches"), e.patches_ = [], e.inversePatches_ = [], e.patchListener_ = t);
}
function hn(e) {
  yn(e), e.drafts_.forEach(cl), e.drafts_ = null;
}
function yn(e) {
  e === et && (et = e.parent_);
}
function Sr(e) {
  return et = ll(et, e);
}
function cl(e) {
  const t = e[se];
  t.type_ === 0 || t.type_ === 1 ? t.revoke_() : t.revoked_ = !0;
}
function xr(e, t) {
  t.unfinalizedDrafts_ = t.drafts_.length;
  const n = t.drafts_[0];
  return e !== void 0 && e !== n ? (n[se].modified_ && (hn(t), me(4)), Me(e) && (e = xt(t, e), t.parent_ || wt(t, e)), t.patches_ && Le("Patches").generateReplacementPatches_(n[se].base_, e, t.patches_, t.inversePatches_)) : e = xt(t, n, []), hn(t), t.patches_ && t.patchListener_(t.patches_, t.inversePatches_), e !== go ? e : void 0;
}
function xt(e, t, n) {
  if (Bt(t)) return t;
  const r = t[se];
  if (!r)
    return St(t, (o, i) => wr(e, r, t, o, i, n)), t;
  if (r.scope_ !== e) return t;
  if (!r.modified_)
    return wt(e, r.base_, !0), r.base_;
  if (!r.finalized_) {
    r.finalized_ = !0, r.scope_.unfinalizedDrafts_--;
    const o = r.copy_;
    let i = o, s = !1;
    r.type_ === 3 && (i = new Set(o), o.clear(), s = !0), St(i, (a, l) => wr(e, r, o, a, l, n, s)), wt(e, o, !1), n && e.patches_ && Le("Patches").generatePatches_(r, n, e.patches_, e.inversePatches_);
  }
  return r.copy_;
}
function wr(e, t, n, r, o, i, s) {
  if (Xe(o)) {
    const a = i && t && t.type_ !== 3 && // Set objects are atomic since they have no keys.
    !pn(t.assigned_, r) ? i.concat(r) : void 0, l = xt(e, o, a);
    if (yo(n, r, l), Xe(l))
      e.canAutoFreeze_ = !1;
    else return;
  } else s && n.add(o);
  if (Me(o) && !Bt(o)) {
    if (!e.immer_.autoFreeze_ && e.unfinalizedDrafts_ < 1)
      return;
    xt(e, o), (!t || !t.scope_.parent_) && typeof r != "symbol" && Object.prototype.propertyIsEnumerable.call(n, r) && wt(e, o);
  }
}
function wt(e, t, n = !1) {
  !e.parent_ && e.immer_.autoFreeze_ && e.canAutoFreeze_ && Rn(t, n);
}
function ul(e, t) {
  const n = Array.isArray(e), r = {
    type_: n ? 1 : 0,
    // Track which produce call this is associated with.
    scope_: t ? t.scope_ : vo(),
    // True for both shallow and deep changes.
    modified_: !1,
    // Used during finalization.
    finalized_: !1,
    // Track which properties have been assigned (true) or deleted (false).
    assigned_: {},
    // The parent draft state.
    parent_: t,
    // The base state.
    base_: e,
    // The base proxy.
    draft_: null,
    // set below
    // The base copy with any updated values.
    copy_: null,
    // Called by the `produce` function.
    revoke_: null,
    isManual_: !1
  };
  let o = r, i = In;
  n && (o = [r], i = tt);
  const {
    revoke: s,
    proxy: a
  } = Proxy.revocable(o, i);
  return r.draft_ = a, r.revoke_ = s, a;
}
var In = {
  get(e, t) {
    if (t === se) return e;
    const n = Re(e);
    if (!pn(n, t))
      return fl(e, n, t);
    const r = n[t];
    return e.finalized_ || !Me(r) ? r : r === en(e.base_, t) ? (tn(e), e.copy_[t] = bn(r, e)) : r;
  },
  has(e, t) {
    return t in Re(e);
  },
  ownKeys(e) {
    return Reflect.ownKeys(Re(e));
  },
  set(e, t, n) {
    const r = bo(Re(e), t);
    if (r != null && r.set)
      return r.set.call(e.draft_, n), !0;
    if (!e.modified_) {
      const o = en(Re(e), t), i = o == null ? void 0 : o[se];
      if (i && i.base_ === n)
        return e.copy_[t] = n, e.assigned_[t] = !1, !0;
      if (il(n, o) && (n !== void 0 || pn(e.base_, t))) return !0;
      tn(e), vn(e);
    }
    return e.copy_[t] === n && // special case: handle new props with value 'undefined'
    (n !== void 0 || t in e.copy_) || // special case: NaN
    Number.isNaN(n) && Number.isNaN(e.copy_[t]) || (e.copy_[t] = n, e.assigned_[t] = !0), !0;
  },
  deleteProperty(e, t) {
    return en(e.base_, t) !== void 0 || t in e.base_ ? (e.assigned_[t] = !1, tn(e), vn(e)) : delete e.assigned_[t], e.copy_ && delete e.copy_[t], !0;
  },
  // Note: We never coerce `desc.value` into an Immer draft, because we can't make
  // the same guarantee in ES5 mode.
  getOwnPropertyDescriptor(e, t) {
    const n = Re(e), r = Reflect.getOwnPropertyDescriptor(n, t);
    return r && {
      writable: !0,
      configurable: e.type_ !== 1 || t !== "length",
      enumerable: r.enumerable,
      value: n[t]
    };
  },
  defineProperty() {
    me(11);
  },
  getPrototypeOf(e) {
    return We(e.base_);
  },
  setPrototypeOf() {
    me(12);
  }
}, tt = {};
St(In, (e, t) => {
  tt[e] = function() {
    return arguments[0] = arguments[0][0], t.apply(this, arguments);
  };
});
tt.deleteProperty = function(e, t) {
  return tt.set.call(this, e, t, void 0);
};
tt.set = function(e, t, n) {
  return In.set.call(this, e[0], t, n, e[0]);
};
function en(e, t) {
  const n = e[se];
  return (n ? Re(n) : e)[t];
}
function fl(e, t, n) {
  var o;
  const r = bo(t, n);
  return r ? "value" in r ? r.value : (
    // This is a very special case, if the prop is a getter defined by the
    // prototype, we should invoke it with the draft as context!
    (o = r.get) == null ? void 0 : o.call(e.draft_)
  ) : void 0;
}
function bo(e, t) {
  if (!(t in e)) return;
  let n = We(e);
  for (; n; ) {
    const r = Object.getOwnPropertyDescriptor(n, t);
    if (r) return r;
    n = We(n);
  }
}
function vn(e) {
  e.modified_ || (e.modified_ = !0, e.parent_ && vn(e.parent_));
}
function tn(e) {
  e.copy_ || (e.copy_ = gn(e.base_, e.scope_.immer_.useStrictShallowCopy_));
}
var dl = class {
  constructor(e) {
    this.autoFreeze_ = !0, this.useStrictShallowCopy_ = !1, this.produce = (t, n, r) => {
      if (typeof t == "function" && typeof n != "function") {
        const i = n;
        n = t;
        const s = this;
        return function(l = i, ...u) {
          return s.produce(l, (f) => n.call(this, f, ...u));
        };
      }
      typeof n != "function" && me(6), r !== void 0 && typeof r != "function" && me(7);
      let o;
      if (Me(t)) {
        const i = Sr(this), s = bn(t, void 0);
        let a = !0;
        try {
          o = n(s), a = !1;
        } finally {
          a ? hn(i) : yn(i);
        }
        return br(i, r), xr(o, i);
      } else if (!t || typeof t != "object") {
        if (o = n(t), o === void 0 && (o = t), o === go && (o = void 0), this.autoFreeze_ && Rn(o, !0), r) {
          const i = [], s = [];
          Le("Patches").generateReplacementPatches_(t, o, i, s), r(i, s);
        }
        return o;
      } else me(1, t);
    }, this.produceWithPatches = (t, n) => {
      if (typeof t == "function")
        return (s, ...a) => this.produceWithPatches(s, (l) => t(l, ...a));
      let r, o;
      return [this.produce(t, n, (s, a) => {
        r = s, o = a;
      }), r, o];
    }, typeof (e == null ? void 0 : e.autoFreeze) == "boolean" && this.setAutoFreeze(e.autoFreeze), typeof (e == null ? void 0 : e.useStrictShallowCopy) == "boolean" && this.setUseStrictShallowCopy(e.useStrictShallowCopy);
  }
  createDraft(e) {
    Me(e) || me(8), Xe(e) && (e = ml(e));
    const t = Sr(this), n = bn(e, void 0);
    return n[se].isManual_ = !0, yn(t), n;
  }
  finishDraft(e, t) {
    const n = e && e[se];
    (!n || !n.isManual_) && me(9);
    const {
      scope_: r
    } = n;
    return br(r, t), xr(void 0, r);
  }
  /**
   * Pass true to automatically freeze all copies created by Immer.
   *
   * By default, auto-freezing is enabled.
   */
  setAutoFreeze(e) {
    this.autoFreeze_ = e;
  }
  /**
   * Pass true to enable strict shallow copy.
   *
   * By default, immer does not copy the object descriptors such as getter, setter and non-enumrable properties.
   */
  setUseStrictShallowCopy(e) {
    this.useStrictShallowCopy_ = e;
  }
  applyPatches(e, t) {
    let n;
    for (n = t.length - 1; n >= 0; n--) {
      const o = t[n];
      if (o.path.length === 0 && o.op === "replace") {
        e = o.value;
        break;
      }
    }
    n > -1 && (t = t.slice(n + 1));
    const r = Le("Patches").applyPatches_;
    return Xe(e) ? r(e, t) : this.produce(e, (o) => r(o, t));
  }
};
function bn(e, t) {
  const n = Dt(e) ? Le("MapSet").proxyMap_(e, t) : Ht(e) ? Le("MapSet").proxySet_(e, t) : ul(e, t);
  return (t ? t.scope_ : vo()).drafts_.push(n), n;
}
function ml(e) {
  return Xe(e) || me(10, e), So(e);
}
function So(e) {
  if (!Me(e) || Bt(e)) return e;
  const t = e[se];
  let n;
  if (t) {
    if (!t.modified_) return t.base_;
    t.finalized_ = !0, n = gn(e, t.scope_.immer_.useStrictShallowCopy_);
  } else
    n = gn(e, !0);
  return St(n, (r, o) => {
    yo(n, r, So(o));
  }), t && (t.finalized_ = !1), n;
}
var ae = new dl(), _r = ae.produce;
ae.produceWithPatches.bind(ae);
ae.setAutoFreeze.bind(ae);
ae.setUseStrictShallowCopy.bind(ae);
ae.applyPatches.bind(ae);
ae.createDraft.bind(ae);
ae.finishDraft.bind(ae);
const {
  useItems: Yl,
  withItemsContextProvider: Ql,
  ItemHandler: Zl
} = Mr("antdx-bubble.list-items"), {
  useItems: pl,
  withItemsContextProvider: gl,
  ItemHandler: Jl
} = Mr("antdx-bubble.list-roles");
function hl(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function yl(e, t = !1) {
  try {
    if (wn(e))
      return e;
    if (t && !hl(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function vl(e, t) {
  return ge(() => yl(e, t), [e, t]);
}
function bl(e, t) {
  return t((r, o) => wn(r) ? o ? (...i) => r(...i, ...e) : r(...e) : r);
}
const Sl = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xl(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return t[n] = wl(n, r), t;
  }, {}) : {};
}
function wl(e, t) {
  return typeof t == "number" && !Sl.includes(e) ? t + "px" : t;
}
function Sn(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const o = c.Children.toArray(e._reactElement.props.children).map((i) => {
      if (c.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Sn(i.props.el);
        return c.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...c.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(ht(c.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, s, l);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const i = r[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Sn(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function _l(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Cr = Ro(({
  slot: e,
  clone: t,
  className: n,
  style: r,
  observeAttributes: o
}, i) => {
  const s = Q(), [a, l] = Qe([]), {
    forceClone: u
  } = ai(), f = u ? !0 : t;
  return we(() => {
    var g;
    if (!s.current || !e)
      return;
    let m = e;
    function d() {
      let p = m;
      if (m.tagName.toLowerCase() === "svelte-slot" && m.children.length === 1 && m.children[0] && (p = m.children[0], p.tagName.toLowerCase() === "react-portal-target" && p.children[0] && (p = p.children[0])), _l(i, p), n && p.classList.add(...n.split(" ")), r) {
        const b = xl(r);
        Object.keys(b).forEach((w) => {
          p.style[w] = b[w];
        });
      }
    }
    let h = null, y = null;
    if (f && window.MutationObserver) {
      let p = function() {
        var _, C, v;
        (_ = s.current) != null && _.contains(m) && ((C = s.current) == null || C.removeChild(m));
        const {
          portals: w,
          clonedElement: E
        } = Sn(e);
        m = E, l(w), m.style.display = "contents", y && clearTimeout(y), y = setTimeout(() => {
          d();
        }, 50), (v = s.current) == null || v.appendChild(m);
      };
      p();
      const b = wi(() => {
        p(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0
          // attributes: observeAttributes ?? (forceClone ? true : false),
        });
      }, 50);
      h = new window.MutationObserver(b), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      m.style.display = "contents", d(), (g = s.current) == null || g.appendChild(m);
    return () => {
      var p, b;
      m.style.display = "", (p = s.current) != null && p.contains(m) && ((b = s.current) == null || b.removeChild(m)), h == null || h.disconnect();
    };
  }, [e, f, n, r, i, o, u]), c.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Cl = ({
  children: e,
  ...t
}) => /* @__PURE__ */ S.jsx(S.Fragment, {
  children: e(t)
});
function El(e) {
  return c.createElement(Cl, {
    children: e
  });
}
function xo(e, t, n) {
  const r = e.filter(Boolean);
  if (r.length !== 0)
    return r.map((o, i) => {
      var u;
      if (typeof o != "object")
        return t != null && t.fallback ? t.fallback(o) : o;
      const s = {
        ...o.props,
        key: ((u = o.props) == null ? void 0 : u.key) ?? (n ? `${n}-${i}` : `${i}`)
      };
      let a = s;
      Object.keys(o.slots).forEach((f) => {
        if (!o.slots[f] || !(o.slots[f] instanceof Element) && !o.slots[f].el)
          return;
        const m = f.split(".");
        m.forEach((b, w) => {
          a[b] || (a[b] = {}), w !== m.length - 1 && (a = s[b]);
        });
        const d = o.slots[f];
        let h, y, g = (t == null ? void 0 : t.clone) ?? !1, p = t == null ? void 0 : t.forceClone;
        d instanceof Element ? h = d : (h = d.el, y = d.callback, g = d.clone ?? g, p = d.forceClone ?? p), p = p ?? !!y, a[m[m.length - 1]] = h ? y ? (...b) => (y(m[m.length - 1], b), /* @__PURE__ */ S.jsx(kn, {
          ...o.ctx,
          params: b,
          forceClone: p,
          children: /* @__PURE__ */ S.jsx(Cr, {
            slot: h,
            clone: g
          })
        })) : El((b) => /* @__PURE__ */ S.jsx(kn, {
          ...o.ctx,
          forceClone: p,
          children: /* @__PURE__ */ S.jsx(Cr, {
            ...b,
            slot: h,
            clone: g
          })
        })) : a[m[m.length - 1]], a = s;
      });
      const l = (t == null ? void 0 : t.children) || "children";
      return o[l] ? s[l] = xo(o[l], t, `${i}`) : t != null && t.children && (s[l] = void 0, Reflect.deleteProperty(s, l)), s;
    });
}
const wo = Symbol();
function Tl(e, t) {
  return bl(t, (n) => {
    var r, o;
    return {
      ...e,
      avatar: wn(e.avatar) ? n(e.avatar) : ve(e.avatar) ? {
        ...e.avatar,
        icon: n((r = e.avatar) == null ? void 0 : r.icon),
        src: n((o = e.avatar) == null ? void 0 : o.src)
      } : e.avatar,
      footer: n(e.footer),
      header: n(e.header),
      loadingRender: n(e.loadingRender, !0),
      messageRender: n(e.messageRender, !0)
    };
  });
}
function $l({
  roles: e,
  preProcess: t,
  postProcess: n
}, r = []) {
  const o = vl(e), i = ne(t), s = ne(n), {
    items: {
      roles: a
    }
  } = pl(), l = ge(() => {
    var f;
    return e || ((f = xo(a, {
      clone: !0,
      forceClone: !0
    })) == null ? void 0 : f.reduce((m, d) => (d.role !== void 0 && (m[d.role] = d), m), {}));
  }, [a, e]), u = ge(() => (f, m) => {
    const d = m ?? f[wo], h = i(f, d) || f;
    if (h.role && (l || {})[h.role])
      return Tl((l || {})[h.role], [h, d]);
    let y;
    return y = s(h, d), y || {
      messageRender(g) {
        return /* @__PURE__ */ S.jsx(S.Fragment, {
          children: ve(g) ? JSON.stringify(g) : g
        });
      }
    };
  }, [l, s, i, ...r]);
  return o || u;
}
function Pl(e) {
  const [t, n] = Qe(!1), r = Q(0), o = Q(!0), i = Q(!0), {
    autoScroll: s,
    ref: a,
    value: l
  } = e, u = ne(() => {
    a.current && (i.current = !0, a.current.scrollTo({
      offset: a.current.nativeElement.scrollHeight,
      behavior: "instant"
    }), n(!1));
  }), f = ne(() => {
    if (!a.current)
      return !1;
    const m = a.current.nativeElement, d = m.scrollHeight, {
      scrollTop: h,
      clientHeight: y
    } = m;
    return d - (h + y) < 100;
  });
  return we(() => {
    a.current && s && l.length && (l.length !== r.current && (o.current = !0), o.current ? u() : f() || n(!0), r.current = l.length);
  }, [l, a, s, u, f]), we(() => {
    if (a.current && s) {
      const m = a.current.nativeElement;
      let d = 0, h = 0;
      const y = (g) => {
        const p = g.target;
        i.current ? i.current = !1 : p.scrollTop < d && p.scrollHeight >= h ? o.current = !1 : f() && (o.current = !0), d = p.scrollTop, h = p.scrollHeight, f() && n(!1);
      };
      return m.addEventListener("scroll", y), () => {
        m.removeEventListener("scroll", y);
      };
    }
  }, []), {
    showScrollButton: t,
    scrollToBottom: u
  };
}
new Intl.Collator(0, {
  numeric: 1
}).compare;
typeof process < "u" && process.versions && process.versions.node;
var xe;
class ec extends TransformStream {
  /** Constructs a new instance. */
  constructor(n = {
    allowCR: !1
  }) {
    super({
      transform: (r, o) => {
        for (r = ze(this, xe) + r; ; ) {
          const i = r.indexOf(`
`), s = n.allowCR ? r.indexOf("\r") : -1;
          if (s !== -1 && s !== r.length - 1 && (i === -1 || i - 1 > s)) {
            o.enqueue(r.slice(0, s)), r = r.slice(s + 1);
            continue;
          }
          if (i === -1) break;
          const a = r[i - 1] === "\r" ? i - 1 : i;
          o.enqueue(r.slice(0, a)), r = r.slice(i + 1);
        }
        Fn(this, xe, r);
      },
      flush: (r) => {
        if (ze(this, xe) === "") return;
        const o = n.allowCR && ze(this, xe).endsWith("\r") ? ze(this, xe).slice(0, -1) : ze(this, xe);
        r.enqueue(o);
      }
    });
    Nn(this, xe, "");
  }
}
xe = new WeakMap();
function Rl(e) {
  try {
    const t = new URL(e);
    return t.protocol === "http:" || t.protocol === "https:";
  } catch {
    return !1;
  }
}
function Il() {
  const e = document.querySelector(".gradio-container");
  if (!e)
    return "";
  const t = e.className.match(/gradio-container-(.+)/);
  return t ? t[1] : "";
}
const Ml = +Il()[0];
function xn(e, t, n) {
  const r = Ml >= 5 ? "gradio_api/" : "";
  return e == null ? n ? `/proxy=${n}${r}file=` : `${t}${r}file=` : Rl(e) ? e : n ? `/proxy=${n}${r}file=${e}` : `${t}/${r}file=${e}`;
}
const Ll = (e) => !!e.url;
function _o(e, t, n) {
  if (e)
    return Ll(e) ? e.url : typeof e == "string" ? e.startsWith("http") ? e : xn(e, t, n) : e;
}
const Nl = ({
  options: e,
  urlProxyUrl: t,
  urlRoot: n,
  onWelcomePromptSelect: r
}) => {
  var a;
  const {
    prompts: o,
    ...i
  } = e, s = ge(() => he(o || {}, {
    omitNull: !0
  }), [o]);
  return /* @__PURE__ */ S.jsxs(_e, {
    vertical: !0,
    gap: "middle",
    children: [/* @__PURE__ */ S.jsx(rl, {
      ...i,
      icon: _o(i.icon, n, t),
      styles: {
        ...i == null ? void 0 : i.styles,
        icon: {
          flexShrink: 0,
          ...(a = i == null ? void 0 : i.styles) == null ? void 0 : a.icon
        }
      },
      classNames: i.class_names,
      className: k(i.elem_classes),
      style: i.elem_style
    }), /* @__PURE__ */ S.jsx(Pn, {
      ...s,
      classNames: s == null ? void 0 : s.class_names,
      className: k(s == null ? void 0 : s.elem_classes),
      style: s == null ? void 0 : s.elem_style,
      onItemClick: ({
        data: l
      }) => {
        r({
          value: l
        });
      }
    })]
  });
}, Er = Symbol(), Tr = Symbol(), $r = Symbol(), nn = Symbol(), Fl = (e) => e ? typeof e == "string" ? {
  src: e
} : ((n) => !!n.url)(e) ? {
  src: e.url
} : e.src ? {
  ...e,
  src: typeof e.src == "string" ? e.src : e.src.url
} : e : void 0, Ol = (e) => typeof e == "string" ? [{
  type: "text",
  content: e
}] : Array.isArray(e) ? e.map((t) => typeof t == "string" ? {
  type: "text",
  content: t
} : t) : ve(e) ? [e] : [], jl = (e, t) => {
  if (typeof e == "string")
    return t[0];
  if (Array.isArray(e)) {
    const n = [...e];
    return Object.keys(t).forEach((r) => {
      const o = n[r];
      typeof o == "string" ? n[r] = t[r] : n[r] = {
        ...o,
        content: t[r]
      };
    }), n;
  }
  return ve(e) ? {
    ...e,
    content: t[0]
  } : e;
}, Co = (e, t, n) => typeof e == "string" ? e : Array.isArray(e) ? e.map((r) => Co(r, t, n)).filter(Boolean).join(`
`) : ve(e) ? e.copyable ?? !0 ? typeof e.content == "string" ? e.content : e.type === "file" ? JSON.stringify(e.content.map((r) => _o(r, t, n))) : JSON.stringify(e.content) : "" : JSON.stringify(e), Eo = (e, t) => (e || []).map((n) => ({
  ...t(n),
  children: Array.isArray(n.children) ? Eo(n.children, t) : void 0
})), kl = ({
  content: e,
  className: t,
  style: n,
  disabled: r,
  urlRoot: o,
  urlProxyUrl: i,
  onCopy: s
}) => {
  const a = ge(() => Co(e, o, i), [e, i, o]), l = Q(null);
  return /* @__PURE__ */ S.jsx(Te.Text, {
    copyable: {
      tooltips: !1,
      onCopy() {
        s == null || s(a);
      },
      text: a,
      icon: [/* @__PURE__ */ S.jsx(ie, {
        ref: l,
        variant: "text",
        color: "default",
        disabled: r,
        size: "small",
        className: t,
        style: n,
        icon: /* @__PURE__ */ S.jsx(Zo, {})
      }, "copy"), /* @__PURE__ */ S.jsx(ie, {
        variant: "text",
        color: "default",
        size: "small",
        disabled: r,
        className: t,
        style: n,
        icon: /* @__PURE__ */ S.jsx(Rr, {})
      }, "copied")]
    }
  });
}, Al = ({
  action: e,
  disabledActions: t,
  message: n,
  onCopy: r,
  onDelete: o,
  onEdit: i,
  onLike: s,
  onRetry: a,
  urlRoot: l,
  urlProxyUrl: u
}) => {
  var h;
  const f = Q(), d = (() => {
    var b, w;
    const {
      action: y,
      disabled: g,
      disableHandler: p
    } = ve(e) ? {
      action: e.action,
      disabled: (t == null ? void 0 : t.includes(e.action)) || !!e.disabled,
      disableHandler: !!e.popconfirm
    } : {
      action: e,
      disabled: (t == null ? void 0 : t.includes(e)) || !1,
      disableHandler: !1
    };
    switch (y) {
      case "copy":
        return /* @__PURE__ */ S.jsx(kl, {
          disabled: g,
          content: n.content,
          onCopy: r,
          urlRoot: l,
          urlProxyUrl: u
        });
      case "like":
        return f.current = () => s(!0), /* @__PURE__ */ S.jsx(ie, {
          variant: "text",
          color: ((b = n.meta) == null ? void 0 : b.feedback) === "like" ? "primary" : "default",
          disabled: g,
          size: "small",
          icon: /* @__PURE__ */ S.jsx(Qo, {}),
          onClick: () => {
            !p && s(!0);
          }
        });
      case "dislike":
        return f.current = () => s(!1), /* @__PURE__ */ S.jsx(ie, {
          variant: "text",
          color: ((w = n.meta) == null ? void 0 : w.feedback) === "dislike" ? "primary" : "default",
          size: "small",
          icon: /* @__PURE__ */ S.jsx(Yo, {}),
          disabled: g,
          onClick: () => !p && s(!1)
        });
      case "retry":
        return f.current = a, /* @__PURE__ */ S.jsx(ie, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(qo, {}),
          onClick: () => !p && a()
        });
      case "edit":
        return f.current = i, /* @__PURE__ */ S.jsx(ie, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(Ko, {}),
          onClick: () => !p && i()
        });
      case "delete":
        return f.current = o, /* @__PURE__ */ S.jsx(ie, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(Go, {}),
          onClick: () => !p && o()
        });
      default:
        return null;
    }
  })();
  if (ve(e)) {
    const y = {
      ...typeof e.popconfirm == "string" ? {
        title: e.popconfirm
      } : {
        ...e.popconfirm,
        title: (h = e.popconfirm) == null ? void 0 : h.title
      },
      onConfirm() {
        var g;
        (g = f.current) == null || g.call(f);
      }
    };
    return c.createElement(e.popconfirm ? ri : c.Fragment, e.popconfirm ? y : void 0, c.createElement(e.tooltip ? oi : c.Fragment, e.tooltip ? typeof e.tooltip == "string" ? {
      title: e.tooltip
    } : e.tooltip : void 0, d));
  }
  return d;
}, zl = ({
  isEditing: e,
  onEditCancel: t,
  onEditConfirm: n,
  onCopy: r,
  onEdit: o,
  onLike: i,
  onDelete: s,
  onRetry: a,
  editValues: l,
  message: u,
  extra: f,
  index: m,
  actions: d,
  disabledActions: h,
  urlRoot: y,
  urlProxyUrl: g
}) => e ? /* @__PURE__ */ S.jsxs(_e, {
  justify: "end",
  children: [/* @__PURE__ */ S.jsx(ie, {
    variant: "text",
    color: "default",
    size: "small",
    icon: /* @__PURE__ */ S.jsx(Uo, {}),
    onClick: () => {
      t == null || t();
    }
  }), /* @__PURE__ */ S.jsx(ie, {
    variant: "text",
    color: "default",
    size: "small",
    icon: /* @__PURE__ */ S.jsx(Rr, {}),
    onClick: () => {
      const p = jl(u.content, l);
      n == null || n({
        index: m,
        value: p,
        previous_value: u.content
      });
    }
  })]
}) : /* @__PURE__ */ S.jsx(_e, {
  justify: "space-between",
  align: "center",
  gap: f && (d != null && d.length) ? "small" : void 0,
  children: (u.role === "user" ? ["extra", "actions"] : ["actions", "extra"]).map((p) => {
    switch (p) {
      case "extra":
        return /* @__PURE__ */ S.jsx(Te.Text, {
          type: "secondary",
          children: f
        }, "extra");
      case "actions":
        return /* @__PURE__ */ S.jsx("div", {
          children: (d || []).map((b, w) => /* @__PURE__ */ S.jsx(Al, {
            urlRoot: y,
            urlProxyUrl: g,
            action: b,
            disabledActions: h,
            message: u,
            onCopy: (E) => r({
              value: E,
              index: m
            }),
            onDelete: () => s({
              index: m,
              value: u.content
            }),
            onEdit: () => o(m),
            onLike: (E) => i == null ? void 0 : i({
              value: u.content,
              liked: E,
              index: m
            }),
            onRetry: () => a == null ? void 0 : a({
              index: m,
              value: u.content
            })
          }, `${b}-${w}`))
        }, "actions");
    }
  })
}), Dl = ({
  markdownConfig: e,
  title: t
}) => t ? e.renderMarkdown ? /* @__PURE__ */ S.jsx(vt, {
  ...e,
  value: t
}) : /* @__PURE__ */ S.jsx(S.Fragment, {
  children: t
}) : null, Hl = (e, t, n) => e ? typeof e == "string" ? {
  url: e.startsWith("http") ? e : xn(e, t, n),
  uid: e,
  name: e.split("/").pop()
} : {
  ...e,
  uid: e.uid || e.path || e.url,
  name: e.name || e.orig_name || (e.url || e.path).split("/").pop(),
  url: e.url || xn(e.path, t, n)
} : {}, Bl = ({
  value: e,
  urlProxyUrl: t,
  urlRoot: n,
  options: r
}) => /* @__PURE__ */ S.jsx(_e, {
  gap: "small",
  wrap: !0,
  ...r,
  children: e == null ? void 0 : e.map((o, i) => {
    const s = Hl(o, n, t);
    return /* @__PURE__ */ S.jsx(fo.FileCard, {
      item: s
    }, `${s.uid}-${i}`);
  })
}), Vl = ({
  value: e,
  options: t,
  onItemClick: n
}) => {
  const {
    elem_style: r,
    elem_classes: o,
    class_names: i,
    styles: s,
    ...a
  } = t;
  return /* @__PURE__ */ S.jsx(Pn, {
    ...a,
    classNames: i,
    className: k(o),
    style: r,
    styles: s,
    items: e,
    onItemClick: ({
      data: l
    }) => {
      n(l);
    }
  });
}, Pr = ({
  value: e,
  options: t
}) => {
  const {
    renderMarkdown: n,
    ...r
  } = t;
  return /* @__PURE__ */ S.jsx(S.Fragment, {
    children: n ? /* @__PURE__ */ S.jsx(vt, {
      ...r,
      value: e
    }) : e
  });
}, Wl = ({
  value: e,
  options: t
}) => {
  const {
    renderMarkdown: n,
    status: r,
    title: o,
    ...i
  } = t, [s, a] = Qe(() => r !== "done");
  return we(() => {
    a(r !== "done");
  }, [r]), /* @__PURE__ */ S.jsx(S.Fragment, {
    children: /* @__PURE__ */ S.jsx(ii, {
      activeKey: s ? ["tool"] : [],
      onChange: () => {
        a(!s);
      },
      items: [{
        key: "tool",
        label: n ? /* @__PURE__ */ S.jsx(vt, {
          ...i,
          value: o
        }) : o,
        children: n ? /* @__PURE__ */ S.jsx(vt, {
          ...i,
          value: e
        }) : e
      }]
    })
  });
}, Xl = ["text", "tool"], Ul = ({
  isEditing: e,
  index: t,
  message: n,
  isLastMessage: r,
  markdownConfig: o,
  onEdit: i,
  onSuggestionSelect: s,
  urlProxyUrl: a,
  urlRoot: l
}) => {
  const u = Q(null), f = () => Ol(n.content).map((d, h) => {
    const y = () => {
      var g;
      if (e && (d.editable ?? !0) && Xl.includes(d.type)) {
        const p = d.content, b = (g = u.current) == null ? void 0 : g.getBoundingClientRect().width;
        return /* @__PURE__ */ S.jsx("div", {
          style: {
            width: b,
            minWidth: 200,
            maxWidth: "100%"
          },
          children: /* @__PURE__ */ S.jsx(si.TextArea, {
            autoSize: {
              minRows: 1,
              maxRows: 10
            },
            defaultValue: p,
            onChange: (w) => {
              i(h, w.target.value);
            }
          })
        });
      }
      switch (d.type) {
        case "text":
          return /* @__PURE__ */ S.jsx(Pr, {
            value: d.content,
            options: he({
              ...o,
              ...mt(d.options)
            }, {
              omitNull: !0
            })
          });
        case "tool":
          return /* @__PURE__ */ S.jsx(Wl, {
            value: d.content,
            options: he({
              ...o,
              ...mt(d.options)
            }, {
              omitNull: !0
            })
          });
        case "file":
          return /* @__PURE__ */ S.jsx(Bl, {
            value: d.content,
            urlRoot: l,
            urlProxyUrl: a,
            options: he(d.options || {}, {
              omitNull: !0
            })
          });
        case "suggestion":
          return /* @__PURE__ */ S.jsx(Vl, {
            value: r ? d.content : Eo(d.content, (p) => ({
              ...p,
              disabled: p.disabled ?? !0
            })),
            options: he(d.options || {}, {
              omitNull: !0
            }),
            onItemClick: (p) => {
              s({
                index: t,
                value: p
              });
            }
          });
        default:
          return typeof d.content != "string" ? null : /* @__PURE__ */ S.jsx(Pr, {
            value: d.content,
            options: he({
              ...o,
              ...mt(d.options)
            }, {
              omitNull: !0
            })
          });
      }
    };
    return /* @__PURE__ */ S.jsx(c.Fragment, {
      children: y()
    }, h);
  });
  return /* @__PURE__ */ S.jsx("div", {
    ref: u,
    children: /* @__PURE__ */ S.jsx(_e, {
      vertical: !0,
      gap: "small",
      children: f()
    })
  });
}, tc = qi(gl(["roles"], ({
  id: e,
  className: t,
  style: n,
  height: r,
  minHeight: o,
  maxHeight: i,
  value: s,
  roles: a,
  urlRoot: l,
  urlProxyUrl: u,
  themeMode: f,
  autoScroll: m = !0,
  markdownConfig: d,
  welcomeConfig: h,
  userConfig: y,
  botConfig: g,
  onValueChange: p,
  onCopy: b,
  onChange: w,
  onEdit: E,
  onRetry: _,
  onDelete: C,
  onLike: v,
  onSuggestionSelect: x,
  onWelcomePromptSelect: P
}) => {
  const N = ge(() => ({
    variant: "borderless",
    ...h ? he(h, {
      omitNull: !0
    }) : {}
  }), [h]), O = ge(() => ({
    lineBreaks: !0,
    renderMarkdown: !0,
    ...mt(d),
    urlRoot: l,
    themeMode: f
  }), [d, f, l]), I = ge(() => y ? he(y, {
    omitNull: !0
  }) : {}, [y]), T = ge(() => g ? he(g, {
    omitNull: !0
  }) : {}, [g]), A = ge(() => {
    const $ = (s || []).map((G, H) => {
      const Se = H === s.length - 1, fe = he(G, {
        omitNull: !0
      });
      return {
        ...jn(fe, ["header", "footer", "avatar"]),
        [wo]: H,
        [Er]: fe.header,
        [Tr]: fe.footer,
        [$r]: fe.avatar,
        [nn]: Se,
        key: fe.key ?? `${H}`
      };
    }).filter((G) => G.role !== "system");
    return $.length > 0 ? $ : [{
      role: "chatbot-internal-welcome"
    }];
  }, [s]), L = Q(null), [R, F] = Qe(-1), [W, X] = Qe({}), Y = Q(), B = ne(($, G) => {
    X((H) => ({
      ...H,
      [$]: G
    }));
  }), z = ne(w);
  we(() => {
    _i(Y.current, s) || (z(), Y.current = s);
  }, [s, z]);
  const K = ne(($) => {
    x == null || x($);
  }), J = ne(($) => {
    P == null || P($);
  }), U = ne(($) => {
    _ == null || _($);
  }), oe = ne(($) => {
    F($);
  }), Ne = ne(() => {
    F(-1);
  }), ue = ne(($) => {
    F(-1), p([...s.slice(0, $.index), {
      ...s[$.index],
      content: $.value
    }, ...s.slice($.index + 1)]), E == null || E($);
  }), qe = ne(($) => {
    b == null || b($);
  }), Fe = ne(($) => {
    v == null || v($), p(_r(s, (G) => {
      const H = G[$.index].meta || {}, Se = $.liked ? "like" : "dislike";
      G[$.index] = {
        ...G[$.index],
        meta: {
          ...H,
          feedback: H.feedback === Se ? null : Se
        }
      };
    }));
  }), Oe = ne(($) => {
    p(_r(s, (G) => {
      G.splice($.index, 1);
    })), C == null || C($);
  }), je = $l({
    roles: a,
    preProcess($, G) {
      var H, Se, fe, Ae;
      return {
        ...$,
        style: $.elem_style,
        className: k($.elem_classes, "ms-gr-pro-chatbot-message"),
        classNames: {
          ...$.class_names,
          avatar: k((H = $.class_names) == null ? void 0 : H.avatar, "ms-gr-pro-chatbot-message-avatar"),
          header: k((Se = $.class_names) == null ? void 0 : Se.header, "ms-gr-pro-chatbot-message-header"),
          footer: k((fe = $.class_names) == null ? void 0 : fe.footer, "ms-gr-pro-chatbot-message-footer", G === R ? "ms-gr-pro-chatbot-message-footer-editing" : void 0),
          content: k((Ae = $.class_names) == null ? void 0 : Ae.content, "ms-gr-pro-chatbot-message-content")
        }
      };
    },
    postProcess($, G) {
      const H = $.role === "user";
      switch ($.role) {
        case "chatbot-internal-welcome":
          return {
            variant: "borderless",
            styles: {
              content: {
                width: "100%"
              }
            },
            messageRender() {
              return /* @__PURE__ */ S.jsx(Nl, {
                urlRoot: l,
                urlProxyUrl: u,
                options: N || {},
                onWelcomePromptSelect: J
              });
            }
          };
        case "user":
        case "assistant":
          return {
            ...jn(H ? I : T, ["actions", "avatar", "header"]),
            ...$,
            style: {
              ...H ? I == null ? void 0 : I.style : T == null ? void 0 : T.style,
              ...$.style
            },
            className: k($.className, H ? I == null ? void 0 : I.elem_classes : T == null ? void 0 : T.elem_classes),
            header: /* @__PURE__ */ S.jsx(Dl, {
              title: $[Er] ?? (H ? I == null ? void 0 : I.header : T == null ? void 0 : T.header),
              markdownConfig: O
            }),
            avatar: Fl($[$r] ?? (H ? I == null ? void 0 : I.avatar : T == null ? void 0 : T.avatar)),
            footer: $[nn] && ($.loading || $.status === "pending") ? null : /* @__PURE__ */ S.jsx(zl, {
              isEditing: R === G,
              message: $,
              extra: $[Tr] ?? (H ? I == null ? void 0 : I.footer : T == null ? void 0 : T.footer),
              urlRoot: l,
              urlProxyUrl: u,
              editValues: W,
              index: G,
              actions: $.actions ?? (H ? (I == null ? void 0 : I.actions) || [] : (T == null ? void 0 : T.actions) || []),
              disabledActions: $.disabled_actions ?? (H ? (I == null ? void 0 : I.disabled_actions) || [] : (T == null ? void 0 : T.disabled_actions) || []),
              onEditCancel: Ne,
              onEditConfirm: ue,
              onCopy: qe,
              onEdit: oe,
              onDelete: Oe,
              onRetry: U,
              onLike: Fe
            }),
            messageRender() {
              return /* @__PURE__ */ S.jsx(Ul, {
                index: G,
                urlProxyUrl: u,
                urlRoot: l,
                isEditing: R === G,
                message: $,
                isLastMessage: $[nn] || !1,
                markdownConfig: O,
                onEdit: B,
                onSuggestionSelect: K
              });
            }
          };
        default:
          return;
      }
    }
  }, [R, I, N, T, O, W]), {
    scrollToBottom: be,
    showScrollButton: ke
  } = Pl({
    ref: L,
    value: s,
    autoScroll: m
  });
  return /* @__PURE__ */ S.jsxs("div", {
    id: e,
    className: k(t, "ms-gr-pro-chatbot"),
    style: {
      height: r,
      minHeight: o,
      maxHeight: i,
      ...n
    },
    children: [/* @__PURE__ */ S.jsx($n.List, {
      ref: L,
      className: "ms-gr-pro-chatbot-messages",
      autoScroll: !1,
      roles: je,
      items: A
    }), ke && /* @__PURE__ */ S.jsx("div", {
      className: "ms-gr-pro-chatbot-scroll-to-bottom-button",
      children: /* @__PURE__ */ S.jsx(ie, {
        icon: /* @__PURE__ */ S.jsx(Jo, {}),
        shape: "circle",
        variant: "outlined",
        color: "primary",
        onClick: be
      })
    })]
  });
}));
export {
  tc as Chatbot,
  tc as default
};

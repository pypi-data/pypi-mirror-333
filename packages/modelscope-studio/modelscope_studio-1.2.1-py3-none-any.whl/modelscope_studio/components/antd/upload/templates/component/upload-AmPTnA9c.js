import { i as Ce, a as Y, r as Pe, w as D, g as ke, b as Ue } from "./Index-QACKtR19.js";
const R = window.ms_globals.React, me = window.ms_globals.React.useMemo, Fe = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, we = window.ms_globals.React.useState, _e = window.ms_globals.React.useEffect, X = window.ms_globals.ReactDOM.createPortal, Te = window.ms_globals.internalContext.useContextPropsContext, Oe = window.ms_globals.internalContext.ContextPropsProvider, je = window.ms_globals.antd.Upload;
var Ne = /\s/;
function We(e) {
  for (var t = e.length; t-- && Ne.test(e.charAt(t)); )
    ;
  return t;
}
var Ae = /^\s+/;
function De(e) {
  return e && e.slice(0, We(e) + 1).replace(Ae, "");
}
var te = NaN, Me = /^[-+]0x[0-9a-f]+$/i, ze = /^0b[01]+$/i, Be = /^0o[0-7]+$/i, qe = parseInt;
function ne(e) {
  if (typeof e == "number")
    return e;
  if (Ce(e))
    return te;
  if (Y(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = Y(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = De(e);
  var r = ze.test(e);
  return r || Be.test(e) ? qe(e.slice(2), r ? 2 : 8) : Me.test(e) ? te : +e;
}
function Ge() {
}
var K = function() {
  return Pe.Date.now();
}, He = "Expected a function", Ke = Math.max, Je = Math.min;
function Xe(e, t, r) {
  var i, s, n, o, l, d, h = 0, v = !1, c = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(He);
  t = ne(t) || 0, Y(r) && (v = !!r.leading, c = "maxWait" in r, n = c ? Ke(ne(r.maxWait) || 0, t) : n, w = "trailing" in r ? !!r.trailing : w);
  function f(u) {
    var x = i, k = s;
    return i = s = void 0, h = u, o = e.apply(k, x), o;
  }
  function g(u) {
    return h = u, l = setTimeout(_, t), v ? f(u) : o;
  }
  function S(u) {
    var x = u - d, k = u - h, W = t - x;
    return c ? Je(W, n - k) : W;
  }
  function m(u) {
    var x = u - d, k = u - h;
    return d === void 0 || x >= t || x < 0 || c && k >= n;
  }
  function _() {
    var u = K();
    if (m(u))
      return b(u);
    l = setTimeout(_, S(u));
  }
  function b(u) {
    return l = void 0, w && i ? f(u) : (i = s = void 0, o);
  }
  function p() {
    l !== void 0 && clearTimeout(l), h = 0, i = d = s = l = void 0;
  }
  function a() {
    return l === void 0 ? o : b(K());
  }
  function C() {
    var u = K(), x = m(u);
    if (i = arguments, s = this, d = u, x) {
      if (l === void 0)
        return g(d);
      if (c)
        return clearTimeout(l), l = setTimeout(_, t), f(d);
    }
    return l === void 0 && (l = setTimeout(_, t)), o;
  }
  return C.cancel = p, C.flush = a, C;
}
var he = {
  exports: {}
}, B = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ye = R, Qe = Symbol.for("react.element"), Ze = Symbol.for("react.fragment"), Ve = Object.prototype.hasOwnProperty, $e = Ye.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, et = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ge(e, t, r) {
  var i, s = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (i in t) Ve.call(t, i) && !et.hasOwnProperty(i) && (s[i] = t[i]);
  if (e && e.defaultProps) for (i in t = e.defaultProps, t) s[i] === void 0 && (s[i] = t[i]);
  return {
    $$typeof: Qe,
    type: e,
    key: n,
    ref: o,
    props: s,
    _owner: $e.current
  };
}
B.Fragment = Ze;
B.jsx = ge;
B.jsxs = ge;
he.exports = B;
var F = he.exports;
const {
  SvelteComponent: tt,
  assign: re,
  binding_callbacks: oe,
  check_outros: nt,
  children: ve,
  claim_element: Ie,
  claim_space: rt,
  component_subscribe: ie,
  compute_slots: ot,
  create_slot: it,
  detach: O,
  element: ye,
  empty: se,
  exclude_internal_props: le,
  get_all_dirty_from_scope: st,
  get_slot_changes: lt,
  group_outros: ct,
  init: at,
  insert_hydration: M,
  safe_not_equal: ut,
  set_custom_element_data: be,
  space: dt,
  transition_in: z,
  transition_out: Q,
  update_slot_base: ft
} = window.__gradio__svelte__internal, {
  beforeUpdate: mt,
  getContext: pt,
  onDestroy: wt,
  setContext: _t
} = window.__gradio__svelte__internal;
function ce(e) {
  let t, r;
  const i = (
    /*#slots*/
    e[7].default
  ), s = it(
    i,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ye("svelte-slot"), s && s.c(), this.h();
    },
    l(n) {
      t = Ie(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = ve(t);
      s && s.l(o), o.forEach(O), this.h();
    },
    h() {
      be(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      M(n, t, o), s && s.m(t, null), e[9](t), r = !0;
    },
    p(n, o) {
      s && s.p && (!r || o & /*$$scope*/
      64) && ft(
        s,
        i,
        n,
        /*$$scope*/
        n[6],
        r ? lt(
          i,
          /*$$scope*/
          n[6],
          o,
          null
        ) : st(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (z(s, n), r = !0);
    },
    o(n) {
      Q(s, n), r = !1;
    },
    d(n) {
      n && O(t), s && s.d(n), e[9](null);
    }
  };
}
function ht(e) {
  let t, r, i, s, n = (
    /*$$slots*/
    e[4].default && ce(e)
  );
  return {
    c() {
      t = ye("react-portal-target"), r = dt(), n && n.c(), i = se(), this.h();
    },
    l(o) {
      t = Ie(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), ve(t).forEach(O), r = rt(o), n && n.l(o), i = se(), this.h();
    },
    h() {
      be(t, "class", "svelte-1rt0kpf");
    },
    m(o, l) {
      M(o, t, l), e[8](t), M(o, r, l), n && n.m(o, l), M(o, i, l), s = !0;
    },
    p(o, [l]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, l), l & /*$$slots*/
      16 && z(n, 1)) : (n = ce(o), n.c(), z(n, 1), n.m(i.parentNode, i)) : n && (ct(), Q(n, 1, 1, () => {
        n = null;
      }), nt());
    },
    i(o) {
      s || (z(n), s = !0);
    },
    o(o) {
      Q(n), s = !1;
    },
    d(o) {
      o && (O(t), O(r), O(i)), e[8](null), n && n.d(o);
    }
  };
}
function ae(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function gt(e, t, r) {
  let i, s, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const l = ot(n);
  let {
    svelteInit: d
  } = t;
  const h = D(ae(t)), v = D();
  ie(e, v, (a) => r(0, i = a));
  const c = D();
  ie(e, c, (a) => r(1, s = a));
  const w = [], f = pt("$$ms-gr-react-wrapper"), {
    slotKey: g,
    slotIndex: S,
    subSlotIndex: m
  } = ke() || {}, _ = d({
    parent: f,
    props: h,
    target: v,
    slot: c,
    slotKey: g,
    slotIndex: S,
    subSlotIndex: m,
    onDestroy(a) {
      w.push(a);
    }
  });
  _t("$$ms-gr-react-wrapper", _), mt(() => {
    h.set(ae(t));
  }), wt(() => {
    w.forEach((a) => a());
  });
  function b(a) {
    oe[a ? "unshift" : "push"](() => {
      i = a, v.set(i);
    });
  }
  function p(a) {
    oe[a ? "unshift" : "push"](() => {
      s = a, c.set(s);
    });
  }
  return e.$$set = (a) => {
    r(17, t = re(re({}, t), le(a))), "svelteInit" in a && r(5, d = a.svelteInit), "$$scope" in a && r(6, o = a.$$scope);
  }, t = le(t), [i, s, v, c, l, d, o, n, b, p];
}
class vt extends tt {
  constructor(t) {
    super(), at(this, t, gt, ht, ut, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: Ut
} = window.__gradio__svelte__internal, ue = window.ms_globals.rerender, J = window.ms_globals.tree;
function It(e, t = {}) {
  function r(i) {
    const s = D(), n = new vt({
      ...i,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            ignore: t.ignore,
            slotKey: o.slotKey,
            nodes: []
          }, d = o.parent ?? J;
          return d.nodes = [...d.nodes, l], ue({
            createPortal: X,
            node: J
          }), o.onDestroy(() => {
            d.nodes = d.nodes.filter((h) => h.svelteInstance !== s), ue({
              createPortal: X,
              node: J
            });
          }), l;
        },
        ...i.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((i) => {
    window.ms_globals.initializePromise.then(() => {
      i(r);
    });
  });
}
function yt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function bt(e, t = !1) {
  try {
    if (Ue(e))
      return e;
    if (t && !yt(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function E(e, t) {
  return me(() => bt(e, t), [e, t]);
}
const xt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Et(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const i = e[r];
    return t[r] = St(r, i), t;
  }, {}) : {};
}
function St(e, t) {
  return typeof t == "number" && !xt.includes(e) ? t + "px" : t;
}
function Z(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const s = R.Children.toArray(e._reactElement.props.children).map((n) => {
      if (R.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: l
        } = Z(n.props.el);
        return R.cloneElement(n, {
          ...n.props,
          el: l,
          children: [...R.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return s.originalChildren = e._reactElement.props.children, t.push(X(R.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: s
    }), r)), {
      clonedElement: r,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((s) => {
    e.getEventListeners(s).forEach(({
      listener: o,
      type: l,
      useCapture: d
    }) => {
      r.addEventListener(l, o, d);
    });
  });
  const i = Array.from(e.childNodes);
  for (let s = 0; s < i.length; s++) {
    const n = i[s];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: l
      } = Z(n);
      t.push(...l), r.appendChild(o);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Lt(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const de = Fe(({
  slot: e,
  clone: t,
  className: r,
  style: i,
  observeAttributes: s
}, n) => {
  const o = pe(), [l, d] = we([]), {
    forceClone: h
  } = Te(), v = h ? !0 : t;
  return _e(() => {
    var S;
    if (!o.current || !e)
      return;
    let c = e;
    function w() {
      let m = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (m = c.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), Lt(n, m), r && m.classList.add(...r.split(" ")), i) {
        const _ = Et(i);
        Object.keys(_).forEach((b) => {
          m.style[b] = _[b];
        });
      }
    }
    let f = null, g = null;
    if (v && window.MutationObserver) {
      let m = function() {
        var a, C, u;
        (a = o.current) != null && a.contains(c) && ((C = o.current) == null || C.removeChild(c));
        const {
          portals: b,
          clonedElement: p
        } = Z(e);
        c = p, d(b), c.style.display = "contents", g && clearTimeout(g), g = setTimeout(() => {
          w();
        }, 50), (u = o.current) == null || u.appendChild(c);
      };
      m();
      const _ = Xe(() => {
        m(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0
          // attributes: observeAttributes ?? (forceClone ? true : false),
        });
      }, 50);
      f = new window.MutationObserver(_), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", w(), (S = o.current) == null || S.appendChild(c);
    return () => {
      var m, _;
      c.style.display = "", (m = o.current) != null && m.contains(c) && ((_ = o.current) == null || _.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, v, r, i, n, s, h]), R.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...l);
}), Rt = ({
  children: e,
  ...t
}) => /* @__PURE__ */ F.jsx(F.Fragment, {
  children: e(t)
});
function Ft(e) {
  return R.createElement(Rt, {
    children: e
  });
}
function fe(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? Ft((r) => /* @__PURE__ */ F.jsx(Oe, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ F.jsx(de, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ F.jsx(de, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function T({
  key: e,
  slots: t,
  targets: r
}, i) {
  return t[e] ? (...s) => r ? r.map((n, o) => /* @__PURE__ */ F.jsx(R.Fragment, {
    children: fe(n, {
      clone: !0,
      params: s,
      forceClone: !0
    })
  }, o)) : /* @__PURE__ */ F.jsx(F.Fragment, {
    children: fe(t[e], {
      clone: !0,
      params: s,
      forceClone: !0
    })
  }) : void 0;
}
const Ct = (e) => !!e.name;
function Pt(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Tt = It(({
  slots: e,
  upload: t,
  showUploadList: r,
  progress: i,
  beforeUpload: s,
  customRequest: n,
  previewFile: o,
  isImageUrl: l,
  itemRender: d,
  iconRender: h,
  data: v,
  onChange: c,
  onValueChange: w,
  onRemove: f,
  maxCount: g,
  fileList: S,
  setSlotParams: m,
  ..._
}) => {
  const b = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof r == "object", p = Pt(r), a = E(p.showPreviewIcon), C = E(p.showRemoveIcon), u = E(p.showDownloadIcon), x = E(s), k = E(n), W = E(i == null ? void 0 : i.format), xe = E(o), Ee = E(l), Se = E(d), Le = E(h), Re = E(v), j = pe(!1), [N, q] = we(S);
  _e(() => {
    q(S);
  }, [S]);
  const V = me(() => {
    const U = {};
    return N.map((y) => {
      if (!Ct(y)) {
        const P = y.url || y.path;
        return U[P] || (U[P] = 0), U[P]++, {
          ...y,
          name: y.orig_name || y.path,
          uid: y.uid || P + "-" + U[P],
          status: "done"
        };
      }
      return y;
    }) || [];
  }, [N]);
  return /* @__PURE__ */ F.jsx(je, {
    ..._,
    fileList: V,
    data: Re || v,
    previewFile: xe,
    isImageUrl: Ee,
    maxCount: g,
    itemRender: e.itemRender ? T({
      slots: e,
      key: "itemRender"
    }) : Se,
    iconRender: e.iconRender ? T({
      slots: e,
      key: "iconRender"
    }) : Le,
    customRequest: k || Ge,
    onChange: async (U) => {
      const y = U.file, P = U.fileList, $ = V.findIndex((I) => I.uid === y.uid);
      if ($ !== -1) {
        if (j.current)
          return;
        f == null || f(y);
        const I = N.slice();
        I.splice($, 1), w == null || w(I), c == null || c(I.map((G) => G.path));
      } else {
        if (x && !await x(y, P) || j.current)
          return;
        j.current = !0;
        let I = P.filter((L) => L.status !== "done");
        if (g === 1)
          I = I.slice(0, 1);
        else if (I.length === 0) {
          j.current = !1;
          return;
        } else if (typeof g == "number") {
          const L = g - N.length;
          I = I.slice(0, L < 0 ? 0 : L);
        }
        const G = N;
        q((L) => [...g === 1 ? [] : L, ...I.map((A) => ({
          ...A,
          size: A.size,
          uid: A.uid,
          name: A.name,
          status: "uploading"
        }))]);
        const ee = (await t(I.map((L) => L.originFileObj))).filter(Boolean), H = g === 1 ? ee : [...G, ...ee];
        j.current = !1, q(H), w == null || w(H), c == null || c(H.map((L) => L.path));
      }
    },
    progress: i && {
      ...i,
      format: W
    },
    showUploadList: b ? {
      ...p,
      showDownloadIcon: u || p.showDownloadIcon,
      showRemoveIcon: C || p.showRemoveIcon,
      showPreviewIcon: a || p.showPreviewIcon,
      downloadIcon: e["showUploadList.downloadIcon"] ? T({
        slots: e,
        key: "showUploadList.downloadIcon"
      }) : p.downloadIcon,
      removeIcon: e["showUploadList.removeIcon"] ? T({
        slots: e,
        key: "showUploadList.removeIcon"
      }) : p.removeIcon,
      previewIcon: e["showUploadList.previewIcon"] ? T({
        slots: e,
        key: "showUploadList.previewIcon"
      }) : p.previewIcon,
      extra: e["showUploadList.extra"] ? T({
        slots: e,
        key: "showUploadList.extra"
      }) : p.extra
    } : r
  });
});
export {
  Tt as Upload,
  Tt as default
};

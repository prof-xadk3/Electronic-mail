var md5 = new gruft.MD5();
var sha256 = new gruft.SHA256();
// var tiger = new gruft.Tiger192();
const socket = new WebSocket("ws://localhost:55555");

window.nostr = {
  _requests: {},
  _pubkey: null,

  async getPublicKey() {
    if (this._pubkey) return this._pubkey
    this._pubkey = await this._call('getPublicKey', {})
    return this._pubkey
  },

  async signEvent(event) {
    return this._call('signEvent', { event })
  },

  async getRelays() {
    return this._call('getRelays', {})
  },

  nip04: {
    async encrypt(peer, plaintext) {
      return window.nostr._call('nip04.encrypt', { peer, plaintext })
    },

    async decrypt(peer, ciphertext) {
      return window.nostr._call('nip04.decrypt', { peer, ciphertext })
    }
  },

  _call(type, params) {
    return new Promise((resolve, reject) => {
      let id = Math.random().toString().slice(4)
      this._requests[id] = { resolve, reject }
      window.postMessage(
        {
          id,
          ext: 'nos2x',
          type,
          params
        },
        '*'
      )
    })
  }
}

if (window.PublicKeyCredential) {
  alert("Where are ur keys?")
} else {
  alert("Upgrade bro.")
}

window.addEventListener('message', message => {
  if (
    !message.data ||
    message.data.response === null ||
    message.data.response === undefined ||
    message.data.ext !== 'nos2x' ||
    !window.nostr._requests[message.data.id]
  )
    return

  if (message.data.response.error) {
    let error = new Error('nos2x: ' + message.data.response.error.message)
    error.stack = message.data.response.error.stack
    window.nostr._requests[message.data.id].reject(error)
  } else {
    window.nostr._requests[message.data.id].resolve(message.data.response)
  }

  delete window.nostr._requests[message.data.id]
})

// hack to replace nostr:nprofile.../etc links with something else
let replacing = null
document.addEventListener('mousedown', replaceNostrSchemeLink)
async function replaceNostrSchemeLink(e) {
  if (e.target.tagName !== 'A' || !e.target.href.startsWith('nostr:')) return
  if (replacing === false) return

  let response = await window.nostr._call('replaceURL', { url: e.target.href })
  if (response === false) {
    replacing = false
    return
  }

  e.target.href = response
}

echoRelays = [
  "wss://relay.f7z.io",
  "wss://nos.lol",
  "wss://relay.nostr.info",
  "wss://nostr-pub.wellorder.net",
  "wss://relay.current.fyi",
  "wss://relay.nostr.band"
] // #nostr ofc. wait.

document.querySelector('.cmd').onkeydown = (event) => {
  if (event.key === "Enter") {
    console.log("Trigger ===", sha256.digest(event.key));
  }
};

console.log(echoRelays);

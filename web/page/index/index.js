
// 引入coolsite360交互配置设定
require('coolsite.config.js');
var QQMapWX = require('../../libs/qqmap-wx-jssdk.js');
var qqmapsdk = new QQMapWX({
  key: '3JXBZ-H32W5-MM5IT-QCQPN-V5ZZ7-CLB5J'
})
// 获取全局应用程序实例对象
var app = getApp();

// 创建页面实例对象
Page({
  /**
   * 页面名称
   */
  name: "index",
  /**
   * 页面的初始数据
   */

  data: {
    "location": "未知",
    "lists": ""
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad () {
    // 注册coolsite360交互模块
    app.coolsite360.register(this);
    this.change_label({currentTarget:{dataset:{lid: "2"}}})
    this.getUserScope()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow () {
    // 执行coolsite360交互组件展示
    app.coolsite360.onShow(this);
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh () {
    
  },

  getLocation: function () {
    var that = this
    wx.getLocation({
      success: function (e) {
        qqmapsdk.reverseGeocoder({
          location: {
            latitude: e.latitude,
            longitude: e.longitude
          },
          success(d) {
            that.setData({
              'location': d.result.ad_info.city
            })
            that.change_label({ "currentTarget": { "dataset": { "lid": "2" } } })
          },
          fail(d) {
            console.log(d)
          }
        })
      },
    })
  },

  go_to_user: function(e){
    wx.navigateTo({
      url: '../user/user',
    })
  },

  go_to_search: function(e){
    wx.navigateTo({
      url: '../search/search',
    })
  },

  
  goToMore: function(e){
    console.log(e)
    wx.navigateTo({
      url: '../more/more?tid='+e.target.dataset.tid,
    })
  },

  goToDetail: function (e) {
    var ctid = e.currentTarget.dataset.ctid
    this.add_history(ctid)
    if (e.currentTarget.dataset.lid == '2') {
      wx.navigateTo({
        url: '../scene/scene?ctid=' + ctid,
      })
    } else {
      wx.navigateTo({
        url: '../fc/fc?ctid=' + ctid,
      })
    }

  },

  change_label: function (e) {
    console.log(e)
    var that = this
    wx.request({
      url: 'http://localhost:5000' + '/recommend/'+ that.data.location + '/' + e.currentTarget.dataset.lid,
      method: 'GET',
      success(e) {
        that.setData({
          "lists": e.data.content
        })
      }
    })
  },
  add_history(ctid){
    wx.request({
      url: 'http://localhost:5000' + '/historys/add',
      method: 'POST',
      data: {
        'ctid': ctid,
        'uid': app.uid
      }
    })
  },
  getUserScope() {
    var that = this
    wx.getSetting({
      success(e) {
        if (e.authSetting['scope.userInfo']) {
          wx.login({
            success(e) {
              var code = e.code
              wx.request({
                url: "https://api.weixin.qq.com/sns/jscode2session?appid=" + "wx2ed99e00d8f6e684" + "&secret=" + "7953c7df51cded0d887b34bcc79ed3c8" + "&js_code=" + code + "&grant_type=authorization_code",
                success(e) {
                  wx.request({
                      url: 'http://localhost:5000' + '/user/' + e.data.openid,
                      method: "GET",
                      success(e){
                        console.log(e)
                        app.uid = e.data.content.uid
                      }
                  })
                }
              })
            }
          })
        }else{
          app.uid = ""
        }
      }
    })
    
  }
})


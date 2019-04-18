
// 引入coolsite360交互配置设定
require('coolsite.config.js');

// 获取全局应用程序实例对象
var app = getApp();

// 创建页面实例对象
Page({
  /**
   * 页面名称
   */
  name: "fc",
  /**
   * 页面的初始数据
   */

  data: {
    "image": "",
    "title": "",
    "addr": "",
    "content": "",
    "comments": [],
    "is_keep": false,
    "ctid": ""
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad (options) {
    // 注册coolsite360交互模块
    app.coolsite360.register(this);
    var ctid = options.ctid
    var that = this
    wx.request({
      url: 'http://localhost:5000'+'/contents',
      method: "POST",
      data: {
        "ctid": ctid,
        "uid": app.uid
      },
      success(e){
        console.log(e)
        var result = e.data.content
        that.setData({
          "ctid": ctid,
          "image": result[0]["coverid"],
          "title": result[0]['title'],
          "content": result[0]["content"],
          "addr": result[0]["addr"],
          "is_keep": result[0]['is_keep']
        })
      }
    })
    this.getComments(ctid)
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


  //以下为自定义点击事件
  getComments(ctid) {
    var that = this
    wx.request({
      url: 'http://localhost:5000' + '/comments/' + ctid,
      method: "GET",
      success(e) {
        if (e.data.status == 1) {
          that.setData({
            "comments": e.data.content
          })
        } else {
          that.setData({
            "comments": []
          })
        }

      }
    })
  },
  changeKeep(e){
    console.log(e)
    var keepno = e.currentTarget.dataset.keepno
    var isKeep = this.data.is_keep
    var that = this
    if (keepno == '0') {
      wx.request({
        url: 'http://localhost:5000' + '/keeps/add',
        method: 'POST',
        data: {
          "uid": app.uid,
          "ctid": that.data.ctid
        },
        success(e) {
          if (e.data.status == 1) {
            that.setData({
              "is_keep": true
            })
          }
        }
      })
    } else {
      wx.request({
        url: 'http://localhost:5000' + '/keeps/del',
        method: 'POST',
        data: {
          "uid": app.uid,
          "ctid": that.data.ctid
        },
        success(e) {
          if (e.data.status == 1) {
            that.setData({
              "is_keep": false
            })
          }
        }
      })
    }
  }
  
})


package com.example.service;

import cn.hutool.core.collection.CollectionUtil;
import com.example.dao.FoodsMaterialInfoDao;
import com.example.dao.FoodsMenuInfoDao;
import com.example.entity.FoodsMaterialInfo;
import com.example.vo.FoodsMaterialInfoVo;
import com.example.vo.FoodsMenuInfoVo;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

@Service
public class FoodsMaterialInfoService {

    @Resource
    private FoodsMaterialInfoDao foodsMaterialInfoDao;
    @Resource
    private FoodsMenuInfoDao foodsMenuInfoDao;

    public FoodsMaterialInfo add(FoodsMaterialInfo info) {
        foodsMaterialInfoDao.insertSelective(info);
        return info;
    }

    public void delete(Long id) {
        foodsMaterialInfoDao.deleteByPrimaryKey(id);
    }

    public void update(FoodsMaterialInfo info) {
        foodsMaterialInfoDao.updateByPrimaryKeySelective(info);
    }

    public FoodsMaterialInfoVo findById(Long id) {
        List<FoodsMaterialInfoVo> list = foodsMaterialInfoDao.findByNameAndId(null, id);
        if (!CollectionUtil.isEmpty(list)) {
            return list.get(0);
        }
        return new FoodsMaterialInfoVo();
    }

    public List<FoodsMaterialInfoVo> findAll() {
        return foodsMaterialInfoDao.findByNameAndId("all", null);
    }

    public PageInfo<FoodsMaterialInfoVo> findPage(String name, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<FoodsMaterialInfoVo> info = foodsMaterialInfoDao.findByNameAndId(name, null);
        return PageInfo.of(info);
    }

    public PageInfo<FoodsMenuInfoVo> getRec(String name, Integer pageNum, Integer pageSize) {
        System.out.println("start");
        String[] args1 = {"python",
                "D:\\workspacePy\\Movies_Recommend-master\\Movie_recommendation_system\\test1.py"};
        String ans = "";
        try {
            Process pr = Runtime.getRuntime().exec(args1);
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    pr.getInputStream(),"gbk"));
            String line;
            while ((line = in.readLine())!=null) {
                System.out.println(line);
                ans = line;
            }
            System.out.println("运行py程序结束.....");
            in.close();
//                pr.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
        ans = ans.replace("[", "");
        ans = ans.replace("]", "");
        ans = ans.replaceAll(" ", "");
        ans = ans.replaceAll("\'", "");
        List<String> ListRecommend = Arrays.asList(ans.split(","));
        System.out.println("推荐的列表为:" + ListRecommend);
        PageHelper.startPage(pageNum, pageSize);
        List<FoodsMenuInfoVo> info = foodsMenuInfoDao.findRec(ListRecommend);
        Collections.shuffle(info);
        return PageInfo.of(info);
    }
}

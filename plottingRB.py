import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "serif"
import pandas as pd
from collections import Counter

def read_rb_analytics(file_paths):
	records = []
	for g in file_paths:
    		records.append(pd.read_csv(g))
	redbubble_data = pd.concat(records)

	print('Found Records through:', pd.to_datetime(redbubble_data['Order Date']).max())

	return redbubble_data


def mult_for_order(redbubble_data):

	# add unique for for everything bought.
	redbubble_data1 = pd.DataFrame()
	for indx, r in redbubble_data.iterrows():
    		for k in range(r['Quantity']):
        		redbubble_data1 = redbubble_data1.append(r)
	return redbubble_data1

def clean_names(redbubble_data):
	redbubble_data = redbubble_data.replace({'Coma Cluster from the Legacy Imaging Survey': 'Coma Cluster from the\nLegacy Imaging Survey',
                                        'DESI Legacy Imaging Survey Footprint': 'DESI Legacy Imaging\nSurvey Footprint',
                                        'Desi Coyote - Canis Major': 'Desi Coyote\n(Canis Major)',
                                        'DESI Logo with text':'DESI Logo',
                                        '-':'\n',
                                        'Glossy Sticker':'Sticker',
                                        'Transparent Sticker':'Sticker',
                                        'Premium T-shirt':'T-shirt',
                                        'Graphic T-shirt': 'T-shirt'},
                                        regex=True)
	return redbubble_data


def plot_design_hist(redbubble_data, per_order = False, merge_simillar_names = True, save_path=False):
	
	''' per_order: count each item independently. Otherwise, only count per order (i.e. 10 stickers bought count as once in the plot'''

	title = 'Which designs are popular? (per order)'
	if per_order==False:
		redbubble_data0 = redbubble_data.copy()
		redbubble_data = mult_for_order(redbubble_data0)
		title = 'Which designs are popular?'

	if merge_simillar_names == True:
		redbubble_data = clean_names(redbubble_data)
	
	work_cnt = redbubble_data.groupby(['Work'])['Work'].count().sort_values(ascending=False)
	
	fig = plt.figure(figsize=(12,8), facecolor='w')
	work_cnt.plot.bar(color='cadetblue', edgecolor='teal', width=0.8, alpha=0.5)
	#plt.yticks(np.linspace(0, 20, 6))
	#plt.ylim(0, 24)
	plt.ylabel('Number Ordered', fontsize=12)
	plt.title(title, fontsize=20)
	plt.xlabel('');
	plt.tight_layout();
	if save_path!=False:
		fig.savefig(save_path, dpi=300);


def plot_product_hist(redbubble_data, per_order = False, merge_simillar_names = True, save_path=False):
	
	''' per_order: count each item independently. Otherwise, only count per order (i.e. 10 stickers bought count as once in the plot'''

	title = 'DESI Redbubble Products (per order)'
	if per_order==False:
		redbubble_data0 = redbubble_data.copy()
		redbubble_data = mult_for_order(redbubble_data0)
		title = 'DESI Redbubble Products'

	if merge_simillar_names == True:
		redbubble_data = clean_names(redbubble_data)

	product_cnt = redbubble_data.groupby(['Product'])['Product'].count().sort_values(ascending=False)
	fig = plt.figure(figsize=(10,5), facecolor='w')
	product_cnt.plot.bar(color='lightsteelblue', alpha=.7, edgecolor='midnightblue', width=0.8)
	#plt.yticks(np.linspace(0, 20, 6))
	plt.ylabel('Number Ordered', fontsize=12)
	plt.title(title, fontsize=20)
	plt.xlabel('');
	plt.tight_layout();
	if save_path!=False:
		fig.savefig(save_path, dpi=300);

def print_order_summary(redbubble_data):
	orders_cnt = redbubble_data.groupby(['Order #'])['Order #'].count()
	n_orders = len(orders_cnt)
	print('n orders:', n_orders)
	print('n products:', len(redbubble_data))

def print_most_common_products(redbubble_data, n=10):
	products_types = list(redbubble_data['Product']+redbubble_data['Work'])
	#c = (word for word in products_types if word[:1].issupper())
	#max(set(products_types), key=products_types.count)
	c = Counter(products_types)
	print('Most common products:')
	print([ci for ci in c.most_common(n)])


def cost_estimates(redbubble_data):
	orders_cost = redbubble_data.groupby(['Order #'])['Retail Price (USD)'].sum()

	fig = plt.figure(figsize=(12,5))

	plt.hist(orders_cost, bins=15, alpha=.4, color='mediumseagreen',
        	 label='Manufacturing Cost per Order');

	plt.hist(orders_cost, histtype='step', bins=15, alpha=.8, color='g')

	est_order_cost = orders_cost * 1.07 * 1.28
	plt.hist(est_order_cost, bins=15, alpha=.5, color='lightsteelblue',
         	label='Total estimated order cost \n(assuming 7% sales tax and 30% shipping)')
	plt.hist(est_order_cost, bins=15, alpha=.8, histtype='step', color='steelblue')


	#plt.ylim(0, 17)
	plt.legend(fontsize=12)
	plt.xlabel('[USD]', fontsize=12)
	plt.ylabel('# Orders', fontsize=12)
	plt.title('How much did each person spend?', fontsize=20);

	total_manufactoring_cost = orders_cost.sum()
	total_est = total_manufactoring_cost * 1.07 * 1.3

	print('Av. order est.:', np.mean(est_order_cost))

